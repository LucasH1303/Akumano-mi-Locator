"""
Script genérico para atualizar qualquer Akuma no Mi
Use este script como modelo para atualizar outras frutas

COMO USAR:
1. Modifique a variável FRUIT_ID com o ID da fruta que deseja atualizar (Pegue o ID da fruta no server.py)
2. Modifique os campos desejados abaixo, retirando a "#" 
3. Execute: python update_fruit.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def update_fruit():
    # ========================================
    # CONFIGURAÇÕES - EDITE AQUI
    # ========================================
    
    # ID da fruta que você quer atualizar
    # Exemplos de IDs: "gomu-gomu", "mera-mera", "yami-yami", etc.
    FRUIT_ID = "gomu-gomu"
    
    # Campos de atualização atualizar
    # IMPORTANTE: Só inclua os campos que você quer modificar!
    updates = {
        # "name": "Gomu Gomu no Mi",
        # "japanese_name": "ゴムゴムの実",
        # "type": "Paramecia",
        # "rarity": "Única",
        # "power": "Borracha",
        # "description": "Transforma o corpo em borracha. Verdadeiro nome: Hito Hito no Mi, Modelo: Nika.",
        # "current_user": "Monkey D. Luffy",
        # "previous_users": ["Joy Boy"],
         "price": 1.000000000 ,
        # "available": False,
        # "keywords": ["borracha", "elástico", "esticar", "flexível", "nika"],
        # "locations": ["East Blue (roubada por Shanks)"],
        # "lore": "Fruta lendária guardada pelo Governo Mundial por 800 anos. Seu verdadeiro poder é de um deus da libertação.",
        # "curiosities": [
            # "O Governo Mundial tentou capturá-la por séculos",
            # "Despertada, permite transformar o ambiente em borracha e acessar o Gear 5",
            # "É considerada a fruta mais ridícula do mundo",
        #], 
        # "first_appearance": "Capítulo 1, Episódio 4",
        # "destructive_power": 100,
        # "defense_rating": 75,
        # "speed_rating": 92,
    }
    
    # ========================================
    # CÓDIGO DE ATUALIZAÇÃO - NÃO EDITE
    # ========================================
    
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Verifica se a fruta existe
    fruit = await db.devil_fruits.find_one({"id": FRUIT_ID}, {"_id": 0})
    if not fruit:
        print(f"❌ Erro: Fruta com ID '{FRUIT_ID}' não encontrada!")
        print("\n💡 Dica: Verifique se o ID está correto.")
        print("   Exemplos de IDs válidos: gomu-gomu, mera-mera, yami-yami")
        client.close()
        return
    
    print(f"📋 Fruta encontrada: {fruit['name']}")
    print(f"   ID: {FRUIT_ID}")
    print("\n🔄 Atualizando campos:")
    
    for field, value in updates.items():
        old_value = fruit.get(field, "N/A")
        print(f"   • {field}: {old_value} → {value}")
    
    # Atualiza a fruta
    result = await db.devil_fruits.update_one(
        {"id": FRUIT_ID},
        {"$set": updates}
    )
    
    if result.modified_count > 0:
        print("\n✅ Fruta atualizada com sucesso!")
        
        # Mostra os dados atualizados
        updated_fruit = await db.devil_fruits.find_one({"id": FRUIT_ID}, {"_id": 0})
        print("\n📊 DADOS ATUALIZADOS:")
        print(f"   Nome: {updated_fruit['name']}")
        print(f"   Tipo: {updated_fruit['type']}")
        print(f"   Raridade: {updated_fruit['rarity']}")
        print(f"   Preço: {updated_fruit['price']:,} berries")
        print(f"   Usuário Atual: {updated_fruit.get('current_user', 'Nenhum')}")
        print(f"   Disponível: {'Sim' if updated_fruit.get('available') else 'Não'}")
        print(f"\n   ESTATÍSTICAS:")
        print(f"   • Poder Destrutivo: {updated_fruit.get('destructive_power', 0)}/100")
        print(f"   • Defesa: {updated_fruit.get('defense_rating', 0)}/100")
        print(f"   • Velocidade: {updated_fruit.get('speed_rating', 0)}/100")
    else:
        print("\n⚠️  Nenhuma alteração foi feita (os valores já eram iguais)")
    
    client.close()

if __name__ == "__main__":
    print("=" * 60)
    print("  ATUALIZADOR DE AKUMA NO MI")
    print("=" * 60)
    asyncio.run(update_fruit())
    print("=" * 60)
