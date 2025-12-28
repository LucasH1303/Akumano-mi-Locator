"""
Script para listar todas as Akuma no Mi disponíveis no banco de dados
Use este script para descobrir os IDs das frutas
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def list_all_fruits():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Busca todas as frutas
    fruits = await db.devil_fruits.find({}, {"_id": 0}).to_list(1000)
    
    print("=" * 80)
    print("  📚 LISTA DE TODAS AS AKUMA NO MI NO BANCO DE DADOS")
    print("=" * 80)
    print(f"\n✨ Total de frutas: {len(fruits)}\n")
    
    # Agrupa por tipo
    types = {}
    for fruit in fruits:
        fruit_type = fruit.get('type', 'Desconhecido')
        if fruit_type not in types:
            types[fruit_type] = []
        types[fruit_type].append(fruit)
    
    # Exibe por tipo
    for fruit_type, fruit_list in sorted(types.items()):
        print(f"\n{'=' * 80}")
        print(f"  🔥 TIPO: {fruit_type.upper()} ({len(fruit_list)} frutas)")
        print(f"{'=' * 80}\n")
        
        for fruit in sorted(fruit_list, key=lambda x: x.get('name', '')):
            id_fruit = fruit.get('id', 'N/A')
            name = fruit.get('name', 'N/A')
            rarity = fruit.get('rarity', 'N/A')
            price = fruit.get('price', 0)
            current_user = fruit.get('current_user', 'Nenhum')
            available = fruit.get('available', False)
            
            # Estatísticas
            destructive = fruit.get('destructive_power', 0)
            defense = fruit.get('defense_rating', 0)
            speed = fruit.get('speed_rating', 0)
            
            status_icon = "🟢" if available else "🔴"
            
            print(f"{status_icon} ID: {id_fruit}")
            print(f"   📛 Nome: {name}")
            print(f"   ⭐ Raridade: {rarity}")
            print(f"   💰 Preço: {price:,} berries")
            print(f"   👤 Usuário: {current_user}")
            print(f"   📊 Stats: ATK {destructive} | DEF {defense} | SPD {speed}")
            print(f"   📍 Disponível: {'Sim' if available else 'Não'}")
            print()
    
    print("=" * 80)
    print("\n💡 DICA: Para atualizar uma fruta, use o ID mostrado acima")
    print("   Exemplo: python update_fruit.py")
    print("   E modifique a linha: FRUIT_ID = \"gomu-gomu\"\n")
    print("=" * 80)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(list_all_fruits())
