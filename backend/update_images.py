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
    "gomu-gomu": "https://static.wikia.nocookie.net/onepiece/images/c/c8/Gomu_Gomu_no_Mi_Infobox.png",
    "yami-yami": "https://static.wikia.nocookie.net/onepiece/images/9/94/Yami_Yami_no_Mi_Infobox.png",
    "gura-gura": "https://static.wikia.nocookie.net/onepiece/images/d/d5/Gura_Gura_no_Mi_Infobox.png",
    "pika-pika": "https://static.wikia.nocookie.net/onepiece/images/5/57/Pika_Pika_no_Mi_Infobox.png",
    "magu-magu": "https://static.wikia.nocookie.net/onepiece/images/1/1e/Magu_Magu_no_Mi_Infobox.png",
    "hie-hie": "https://customer-assets.emergentagent.com/job_devil-fruit-db/artifacts/40lnifvw_Hie_Hie_no_Mi.webp",
    "ope-ope": "https://customer-assets.emergentagent.com/job_devil-fruit-db/artifacts/p89k0n3p_Ope_Ope_no_Mi_Infobox.webp",
    "suna-suna": "https://static.wikia.nocookie.net/onepiece/images/b/b6/Suna_Suna_no_Mi_Infobox.png",
    "goro-goro": "https://static.wikia.nocookie.net/onepiece/images/6/6b/Goro_Goro_no_Mi_Infobox.png",
    "mochi-mochi": "https://static.wikia.nocookie.net/onepiece/images/0/04/Mochi_Mochi_no_Mi_Infobox.png",
    "hana-hana": "https://static.wikia.nocookie.net/onepiece/images/5/57/Hana_Hana_no_Mi_Infobox.png",
    "bari-bari": "https://static.wikia.nocookie.net/onepiece/images/5/54/Bari_Bari_no_Mi_Infobox.png",
    "hobi-hobi": "https://static.wikia.nocookie.net/onepiece/images/e/e8/Hobi_Hobi_no_Mi_Infobox.png",
    "zou-zou": "https://static.wikia.nocookie.net/onepiece/images/f/f1/Zou_Zou_no_Mi_Infobox.png",
    "tori-tori-phoenix": "https://static.wikia.nocookie.net/onepiece/images/3/32/Tori_Tori_no_Mi%2C_Model_Phoenix_Infobox.png",
    "ito-ito": "https://static.wikia.nocookie.net/onepiece/images/9/9a/Ito_Ito_no_Mi_Infobox.png",
    "nikyu-nikyu": "https://static.wikia.nocookie.net/onepiece/images/d/d0/Nikyu_Nikyu_no_Mi_Infobox.png",
    "hito-hito-daibutsu": "https://static.wikia.nocookie.net/onepiece/images/3/35/Hito_Hito_no_Mi%2C_Model_Daibutsu_Infobox.png",
    "doku-doku": "https://static.wikia.nocookie.net/onepiece/images/b/b1/Doku_Doku_no_Mi_Infobox.png",
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
