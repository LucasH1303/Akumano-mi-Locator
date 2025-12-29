"""
Script para remover frutas duplicadas do banco de dados
Mantém apenas a primeira ocorrência de cada fruta (por ID)
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def remove_duplicates():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("=" * 70)
    print("  🔍 REMOVENDO FRUTAS DUPLICADAS DO BANCO DE DADOS")
    print("=" * 70)
    
    # Busca todas as frutas
    all_fruits = await db.devil_fruits.find({}).to_list(1000)
    
    print(f"\n📊 Status inicial:")
    print(f"   Total de documentos: {len(all_fruits)}")
    
    # Agrupa frutas por ID
    fruits_by_id = defaultdict(list)
    for fruit in all_fruits:
        fruits_by_id[fruit['id']].append(fruit)
    
    print(f"   IDs únicos: {len(fruits_by_id)}")
    
    # Identifica duplicatas
    duplicates_to_remove = []
    for fruit_id, fruit_list in fruits_by_id.items():
        if len(fruit_list) > 1:
            # Mantém o primeiro, remove os demais
            for fruit in fruit_list[1:]:
                duplicates_to_remove.append(fruit['_id'])
    
    print(f"\n🗑️  Duplicatas a remover: {len(duplicates_to_remove)}")
    
    if duplicates_to_remove:
        print(f"\n🔄 Removendo {len(duplicates_to_remove)} documentos duplicados...")
        
        # Remove as duplicatas
        result = await db.devil_fruits.delete_many({
            '_id': {'$in': duplicates_to_remove}
        })
        
        print(f"   ✅ Removidos: {result.deleted_count} documentos")
        
        # Verifica o resultado final
        final_count = await db.devil_fruits.count_documents({})
        final_fruits = await db.devil_fruits.find({}, {'_id': 0, 'id': 1, 'name': 1}).to_list(1000)
        
        print(f"\n📊 Status final:")
        print(f"   Total de documentos: {final_count}")
        print(f"   IDs únicos: {len(set(f['id'] for f in final_fruits))}")
        
        print(f"\n✨ SUCESSO! Banco de dados limpo!")
        print(f"\n📋 Lista de frutas únicas restantes:")
        
        # Lista as frutas por tipo
        from collections import defaultdict
        by_type = defaultdict(list)
        for fruit in final_fruits:
            # Busca a fruta completa para pegar o tipo
            full_fruit = await db.devil_fruits.find_one({'id': fruit['id']})
            by_type[full_fruit.get('type', 'Desconhecido')].append(fruit)
        
        for fruit_type in sorted(by_type.keys()):
            print(f"\n   {fruit_type}:")
            for fruit in sorted(by_type[fruit_type], key=lambda x: x['name']):
                print(f"   • {fruit['id']} - {fruit['name']}")
    else:
        print("\n✅ Nenhuma duplicata encontrada! Banco já está limpo.")
    
    print("\n" + "=" * 70)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(remove_duplicates())
