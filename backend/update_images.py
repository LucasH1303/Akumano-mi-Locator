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
    "mera-mera": "https://customer-assets.emergentagent.com/job_devil-fruit-db/artifacts/4pt53a9k_Mera_Mera_no_Mi_Infobox.webp",
    "gomu-gomu": "https://vignette.wikia.nocookie.net/onepiece/images/c/c8/Gomu_Gomu_no_Mi_Infobox.png/revision/latest?cb=20230204165957",
    "yami-yami": "https://vignette.wikia.nocookie.net/onepiece/images/9/94/Yami_Yami_no_Mi_Infobox.png/revision/latest?cb=20130503035722",
    "gura-gura": "https://vignette.wikia.nocookie.net/onepiece/images/d/d5/Gura_Gura_no_Mi_Infobox.png/revision/latest?cb=20130808092131",
    "pika-pika": "https://vignette.wikia.nocookie.net/onepiece/images/5/57/Pika_Pika_no_Mi_Infobox.png/revision/latest?cb=20130319225056",
    "magu-magu": "https://vignette.wikia.nocookie.net/onepiece/images/1/1e/Magu_Magu_no_Mi_Infobox.png/revision/latest?cb=20130319225043",
    "hie-hie": "https://customer-assets.emergentagent.com/job_devil-fruit-db/artifacts/40lnifvw_Hie_Hie_no_Mi.webp",
    "ope-ope": "https://customer-assets.emergentagent.com/job_devil-fruit-db/artifacts/p89k0n3p_Ope_Ope_no_Mi_Infobox.webp",
    "suna-suna": "https://i.imgur.com/EsoXsyo.jpeg",
    "goro-goro": "https://vignette.wikia.nocookie.net/onepiece/images/6/6b/Goro_Goro_no_Mi_Infobox.png/revision/latest?cb=20130417030954",
    "mochi-mochi": "https://vignette.wikia.nocookie.net/onepiece/images/0/04/Mochi_Mochi_no_Mi_Infobox.png/revision/latest?cb=20170205150202",
    "hana-hana": "https://vignette.wikia.nocookie.net/onepiece/images/5/57/Hana_Hana_no_Mi_Infobox.png/revision/latest?cb=20130407020855",
    "bari-bari": "https://vignette.wikia.nocookie.net/onepiece/images/5/54/Bari_Bari_no_Mi_Infobox.png/revision/latest?cb=20140421002641",
    "hobi-hobi": "https://vignette.wikia.nocookie.net/onepiece/images/e/e8/Hobi_Hobi_no_Mi_Infobox.png/revision/latest?cb=20140421000841",
    "zou-zou": "https://vignette.wikia.nocookie.net/onepiece/images/f/f1/Zou_Zou_no_Mi_Infobox.png/revision/latest?cb=20130504194643",
    "tori-tori-phoenix": "https://vignette.wikia.nocookie.net/onepiece/images/3/32/Tori_Tori_no_Mi%2C_Model_Phoenix_Infobox.png/revision/latest?cb=20130723050012",
    "ito-ito": "https://vignette.wikia.nocookie.net/onepiece/images/9/9a/Ito_Ito_no_Mi_Infobox.png/revision/latest?cb=20140501185346",
    "nikyu-nikyu": "https://vignette.wikia.nocookie.net/onepiece/images/d/d0/Nikyu_Nikyu_no_Mi_Infobox.png/revision/latest?cb=20130416184338",
    "hito-hito-daibutsu": "https://vignette.wikia.nocookie.net/onepiece/images/3/35/Hito_Hito_no_Mi%2C_Model_Daibutsu_Infobox.png/revision/latest?cb=20130723051107",
    "doku-doku": "https://vignette.wikia.nocookie.net/onepiece/images/b/b1/Doku_Doku_no_Mi_Infobox.png/revision/latest?cb=20130413223959",
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
