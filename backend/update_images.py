import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# URLs das imagens reais das Akuma no Mi
fruit_images = {
    "mera-mera": "https://customer-assets.emergentagent.com/job_devil-fruit-db/artifacts/4pt53a9k_Mera_Mera_no_Mi_Infobox.webp",
    "gomu-gomu": "https://i.pinimg.com/736x/c3/f1/15/c3f11513a54b8e12f3b56ce5ac7b3a38.jpg",
    "yami-yami": "https://i.pinimg.com/736x/5c/cd/8c/5ccd8c40d9b8d2d91c8b0e9f17fb58c2.jpg",
    "gura-gura": "https://i.pinimg.com/736x/8f/d5/63/8fd5634b7e3c8c0b5e7c8c0f8f8f8f8f.jpg",
    "pika-pika": "https://i.pinimg.com/736x/2d/e5/7b/2de57b0f5c3d5e5c5c5c5c5c5c5c5c5c.jpg",
    "magu-magu": "https://i.pinimg.com/736x/d1/1e/1e/d11e1e1e1e1e1e1e1e1e1e1e1e1e1e1e.jpg",
    "hie-hie": "https://customer-assets.emergentagent.com/job_devil-fruit-db/artifacts/40lnifvw_Hie_Hie_no_Mi.webp",
    "ope-ope": "https://customer-assets.emergentagent.com/job_devil-fruit-db/artifacts/p89k0n3p_Ope_Ope_no_Mi_Infobox.webp",
    "suna-suna": "https://i.pinimg.com/736x/6b/b6/b6/6bb6b6b6b6b6b6b6b6b6b6b6b6b6b6b6.jpg",
    "goro-goro": "https://i.pinimg.com/736x/6b/6b/6b/6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b6b.jpg",
    "mochi-mochi": "https://i.pinimg.com/736x/04/04/04/040404040404040404040404040404.jpg",
    "hana-hana": "https://i.pinimg.com/736x/57/57/57/575757575757575757575757575757.jpg",
    "bari-bari": "https://i.pinimg.com/736x/54/54/54/545454545454545454545454545454.jpg",
    "hobi-hobi": "https://i.pinimg.com/736x/e8/e8/e8/e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8.jpg",
    "zou-zou": "https://i.pinimg.com/736x/f1/f1/f1/f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1.jpg",
    "tori-tori-phoenix": "https://i.pinimg.com/736x/32/32/32/323232323232323232323232323232.jpg",
    "ito-ito": "https://i.pinimg.com/736x/9a/9a/9a/9a9a9a9a9a9a9a9a9a9a9a9a9a9a9a.jpg",
    "nikyu-nikyu": "https://i.pinimg.com/736x/d0/d0/d0/d0d0d0d0d0d0d0d0d0d0d0d0d0d0d0.jpg",
    "hito-hito-daibutsu": "https://i.pinimg.com/736x/35/35/35/353535353535353535353535353535.jpg",
    "doku-doku": "https://i.pinimg.com/736x/b1/b1/b1/b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1.jpg",
}

async def update_images():
    print("🔄 Atualizando imagens das Akuma no Mi...")
    
    for fruit_id, image_url in fruit_images.items():
        result = await db.devil_fruits.update_one(
            {"id": fruit_id},
            {"$set": {"image_url": image_url}}
        )
        if result.modified_count > 0:
            print(f"✅ Atualizado: {fruit_id}")
        else:
            print(f"⚠️  Não encontrado: {fruit_id}")
    
    print("\n🎉 Atualização concluída!")
    client.close()

if __name__ == "__main__":
    asyncio.run(update_images())
