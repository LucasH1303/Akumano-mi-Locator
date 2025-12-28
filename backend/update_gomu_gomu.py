"""
Script para atualizar as informações da Gomu Gomu no Mi
Execute este script para modificar os dados da fruta no banco de dados
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def update_gomu_gomu():
    # Conecta ao MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Dados atualizados para a Gomu Gomu no Mi
    updates = {
        "type": "Zoan",  # Alterado de Paramecia para Zoan
        "price": 10000000000,  # 10 bilhões de berries
        "destructive_power": 100,
        "defense_rating": 100,
        "speed_rating": 100
    }
    
    # Atualiza a fruta no banco de dados
    result = await db.devil_fruits.update_one(
        {"id": "gomu-gomu"},
        {"$set": updates}
    )
    
    if result.modified_count > 0:
        print("✅ Gomu Gomu no Mi atualizada com sucesso!")
        print(f"   Tipo: {updates['type']}")
        print(f"   Preço: {updates['price']:,} berries")
        print(f"   Poder Destrutivo: {updates['destructive_power']}/100")
        print(f"   Defesa: {updates['defense_rating']}/100")
        print(f"   Velocidade: {updates['speed_rating']}/100")
        
        # Mostra a fruta atualizada
        updated_fruit = await db.devil_fruits.find_one({"id": "gomu-gomu"}, {"_id": 0})
        print("\n📋 Dados completos atualizados:")
        print(f"   Nome: {updated_fruit['name']}")
        print(f"   Tipo: {updated_fruit['type']}")
        print(f"   Raridade: {updated_fruit['rarity']}")
        print(f"   Preço: {updated_fruit['price']:,} berries")
    else:
        print("❌ Nenhuma fruta foi atualizada. Verifique se o ID está correto.")
    
    client.close()

if __name__ == "__main__":
    print("🔄 Atualizando Gomu Gomu no Mi...")
    asyncio.run(update_gomu_gomu())
