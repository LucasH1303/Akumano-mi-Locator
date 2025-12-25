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
# Usando imagens de alta qualidade de fontes confiáveis
fruit_images = {
    "mera-mera": "https://i.imgur.com/PZSxBG4.jpeg",
    "gomu-gomu": "https://i.imgur.com/z80uFql.jpeg",
    "yami-yami": "https://i.imgur.com/WhGiGKQ.jpeg",
    "gura-gura": "https://i.imgur.com/8SXsOO1.jpeg",
    "pika-pika": "https://i.imgur.com/yYqnjZl.jpeg",
    "magu-magu": "https://i.imgur.com/zX2Dbw5.jpeg",
    "hie-hie": "https://i.imgur.com/e4U3wtZ.jpeg",
    "ope-ope": "https://i.imgur.com/b2DourR.jpeg",
    "suna-suna": "https://i.imgur.com/b7b1JT3.jpeg",
    "goro-goro": "https://i.imgur.com/G6tMkAt.jpeg",
    "mochi-mochi": "https://i.imgur.com/zO3TPRK.jpeg",
    "hana-hana": "https://i.imgur.com/P5DPu2V.jpeg",
    "bari-bari": "https://i.imgur.com/PsGK15z.png",
    "hobi-hobi": "https://i.imgur.com/gKYwHxX.png",
    "zou-zou": "https://i.imgur.com/Ekcxa7k.jpeg",
    "tori-tori-phoenix": "https://i.imgur.com/j7uyr20.jpeg",
    "ito-ito": "https://i.imgur.com/2LYgQ6Y.jpeg",
    "nikyu-nikyu": "https://i.imgur.com/26ANSfZ.jpeg",
    "hito-hito-daibutsu": "https://i.imgur.com/Pf8Q01R.jpeg",
    "doku-doku": "https://i.imgur.com/BLReWM1.png",
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