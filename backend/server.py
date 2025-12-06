from fastapi import FastAPI, APIRouter, Query, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

class DevilFruit(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    japanese_name: str
    type: str
    rarity: str
    power: str
    description: str
    current_user: Optional[str] = None
    previous_users: List[str] = Field(default_factory=list)
    price: int
    available: bool
    keywords: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    lore: str = ""
    curiosities: List[str] = Field(default_factory=list)
    first_appearance: str = ""
    destructive_power: int = 0
    defense_rating: int = 0
    speed_rating: int = 0
    image_url: str = ""
    fighting_styles: List[str] = Field(default_factory=list)

class SearchRequest(BaseModel):
    budget: Optional[int] = None
    fruit_type: Optional[str] = None
    description: Optional[str] = None
    rarity: Optional[str] = None
    fighting_style: Optional[str] = None

@api_router.get("/")
async def root():
    return {"message": "Akuma Finder API"}

@api_router.get("/fruits", response_model=List[DevilFruit])
async def get_all_fruits(
    type: Optional[str] = Query(None),
    rarity: Optional[str] = Query(None),
    available: Optional[bool] = Query(None),
    sort_by: Optional[str] = Query(None)
):
    query = {}
    if type:
        query['type'] = type
    if rarity:
        query['rarity'] = rarity
    if available is not None:
        query['available'] = available
    
    fruits = await db.devil_fruits.find(query, {"_id": 0}).to_list(1000)
    
    if sort_by == "price_asc":
        fruits.sort(key=lambda x: x['price'])
    elif sort_by == "price_desc":
        fruits.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == "name":
        fruits.sort(key=lambda x: x['name'])
    
    return fruits

@api_router.get("/fruits/{fruit_id}", response_model=DevilFruit)
async def get_fruit_by_id(fruit_id: str):
    fruit = await db.devil_fruits.find_one({"id": fruit_id}, {"_id": 0})
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruta não encontrada")
    return fruit

@api_router.post("/search", response_model=List[DevilFruit])
async def search_fruits(search: SearchRequest):
    query = {}
    
    if search.fruit_type:
        query['type'] = search.fruit_type
    
    if search.rarity:
        query['rarity'] = search.rarity
    
    if search.fighting_style:
        query['fighting_styles'] = {"$in": [search.fighting_style]}
    
    fruits = await db.devil_fruits.find(query, {"_id": 0}).to_list(1000)
    
    if search.description:
        desc_lower = search.description.lower()
        filtered = []
        for fruit in fruits:
            keywords_match = any(kw.lower() in desc_lower for kw in fruit.get('keywords', []))
            power_match = desc_lower in fruit.get('power', '').lower()
            desc_match = desc_lower in fruit.get('description', '').lower()
            
            if keywords_match or power_match or desc_match:
                filtered.append(fruit)
        fruits = filtered
    
    if search.budget:
        fruits = [f for f in fruits if f['price'] <= search.budget]
    
    fruits.sort(key=lambda x: (
        1 if x.get('available', False) else 0,
        -sum(k.lower() in search.description.lower() for k in x.get('keywords', [])) if search.description else 0
    ), reverse=True)
    
    return fruits

@api_router.get("/rankings/expensive", response_model=List[DevilFruit])
async def get_most_expensive():
    fruits = await db.devil_fruits.find({}, {"_id": 0}).to_list(1000)
    fruits.sort(key=lambda x: x['price'], reverse=True)
    return fruits[:10]

@api_router.get("/rankings/destructive", response_model=List[DevilFruit])
async def get_most_destructive():
    fruits = await db.devil_fruits.find({}, {"_id": 0}).to_list(1000)
    fruits.sort(key=lambda x: x.get('destructive_power', 0), reverse=True)
    return fruits[:10]

@api_router.get("/rankings/rare", response_model=List[DevilFruit])
async def get_most_rare():
    rarity_order = {"Única": 5, "Mítica": 4, "Muito Rara": 3, "Rara": 2, "Comum": 1}
    fruits = await db.devil_fruits.find({}, {"_id": 0}).to_list(1000)
    fruits.sort(key=lambda x: (rarity_order.get(x.get('rarity', 'Comum'), 0), x['price']), reverse=True)
    return fruits[:10]

@api_router.get("/rankings/defense", response_model=List[DevilFruit])
async def get_best_defense():
    fruits = await db.devil_fruits.find({}, {"_id": 0}).to_list(1000)
    fruits.sort(key=lambda x: x.get('defense_rating', 0), reverse=True)
    return fruits[:10]

@api_router.get("/rankings/speed", response_model=List[DevilFruit])
async def get_best_speed():
    fruits = await db.devil_fruits.find({}, {"_id": 0}).to_list(1000)
    fruits.sort(key=lambda x: x.get('speed_rating', 0), reverse=True)
    return fruits[:10]

@api_router.get("/black-market", response_model=List[DevilFruit])
async def get_black_market():
    fruits = await db.devil_fruits.find({}, {"_id": 0}).to_list(1000)
    return fruits

@api_router.post("/init-database")
async def init_database():
    count = await db.devil_fruits.count_documents({})
    if count > 0:
        return {"message": "Database already initialized", "count": count}
    
    fruits_data = [
        {
            "id": "mera-mera",
            "name": "Mera Mera no Mi",
            "japanese_name": "メラメラの実",
            "type": "Logia",
            "rarity": "Muito Rara",
            "power": "Fogo",
            "description": "Permite ao usuário criar, controlar e se transformar em fogo. Uma das Logias mais poderosas.",
            "current_user": "Sabo",
            "previous_users": ["Portgas D. Ace"],
            "price": 350000000,
            "available": False,
            "keywords": ["fogo", "chamas", "calor", "queimar", "incêndio"],
            "locations": ["Dressrosa (Coliseu)"],
            "lore": "Fruta que pertenceu a Ace, irmão de Luffy. Após sua morte, reapareceu em Dressrosa.",
            "curiosities": [
                "Ace recusou se tornar um Shichibukai graças a essa fruta",
                "Sabo comeu a fruta para honrar a memória de Ace",
                "É inferior à Magu Magu no Mi na hierarquia de temperatura"
            ],
            "first_appearance": "Capítulo 159, Episódio 95",
            "destructive_power": 95,
            "defense_rating": 98,
            "speed_rating": 85,
            "image_url": "https://images.unsplash.com/photo-1705246535209-8c53b6b4f818?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Alta defesa", "Controle elemental"]
        },
        {
            "id": "gomu-gomu",
            "name": "Gomu Gomu no Mi",
            "japanese_name": "ゴムゴムの実",
            "type": "Paramecia",
            "rarity": "Única",
            "power": "Borracha",
            "description": "Transforma o corpo em borracha. Verdadeiro nome: Hito Hito no Mi, Modelo: Nika.",
            "current_user": "Monkey D. Luffy",
            "previous_users": ["Joy Boy"],
            "price": 5000000000,
            "available": False,
            "keywords": ["borracha", "elástico", "esticar", "flexível", "nika"],
            "locations": ["East Blue (roubada por Shanks)"],
            "lore": "Fruta lendária guardada pelo Governo Mundial por 800 anos. Seu verdadeiro poder é de um deus da libertação.",
            "curiosities": [
                "O Governo Mundial tentou capturá-la por séculos",
                "Despertada, permite transformar o ambiente em borracha e acessar o Gear 5",
                "É considerada a fruta mais ridícula do mundo"
            ],
            "first_appearance": "Capítulo 1, Episódio 4",
            "destructive_power": 100,
            "defense_rating": 75,
            "speed_rating": 92,
            "image_url": "https://images.unsplash.com/photo-1583487488041-5ebf7dec1db5?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Combate bruto", "Velocidade", "Melhor mobilidade"]
        },
        {
            "id": "yami-yami",
            "name": "Yami Yami no Mi",
            "japanese_name": "ヤミヤミの実",
            "type": "Logia",
            "rarity": "Única",
            "power": "Escuridão",
            "description": "Permite criar e controlar a escuridão. Pode anular os poderes de outras Akuma no Mi.",
            "current_user": "Marshall D. Teach (Barba Negra)",
            "previous_users": ["Thatch"],
            "price": 4000000000,
            "available": False,
            "keywords": ["escuridão", "trevas", "gravidade", "absorção", "nulificar"],
            "locations": ["Navio do Barba Branca"],
            "lore": "Considerada a mais maligna das Akuma no Mi. Blackbeard procurou por ela durante décadas.",
            "curiosities": [
                "É a única Logia que não torna o usuário intangível",
                "Pode sugar tudo como um buraco negro",
                "Blackbeard matou Thatch para obtê-la"
            ],
            "first_appearance": "Capítulo 440, Episódio 325",
            "destructive_power": 98,
            "defense_rating": 45,
            "speed_rating": 70,
            "image_url": "https://images.unsplash.com/photo-1600788894044-fb8c7d5d9442?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Controle elemental"]
        },
        {
            "id": "gura-gura",
            "name": "Gura Gura no Mi",
            "japanese_name": "グラグラの実",
            "type": "Paramecia",
            "rarity": "Única",
            "power": "Terremoto",
            "description": "Permite criar terremotos e tremores devastadores. Considerada a Paramecia mais destrutiva.",
            "current_user": "Marshall D. Teach (Barba Negra)",
            "previous_users": ["Edward Newgate (Barba Branca)"],
            "price": 5000000000,
            "available": False,
            "keywords": ["terremoto", "tremor", "destruição", "tsunami", "rachadura"],
            "locations": ["Marineford"],
            "lore": "Fruta que deu a Barba Branca o título de homem mais forte do mundo.",
            "curiosities": [
                "Pode destruir o mundo inteiro segundo Sengoku",
                "Blackbeard roubou o poder após a morte de Barba Branca",
                "Causa rachaduras no ar"
            ],
            "first_appearance": "Capítulo 552, Episódio 434",
            "destructive_power": 100,
            "defense_rating": 60,
            "speed_rating": 50,
            "image_url": "https://images.unsplash.com/photo-1588613000171-55fe9ac1e10b?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Combate bruto"]
        },
        {
            "id": "pika-pika",
            "name": "Pika Pika no Mi",
            "japanese_name": "ピカピカの実",
            "type": "Logia",
            "rarity": "Mítica",
            "power": "Luz",
            "description": "Permite criar, controlar e se transformar em luz. Concede velocidade na velocidade da luz.",
            "current_user": "Borsalino (Kizaru)",
            "previous_users": [],
            "price": 3500000000,
            "available": False,
            "keywords": ["luz", "laser", "velocidade", "brilho", "fóton"],
            "locations": ["Marinha (Almirante Kizaru)"],
            "lore": "Uma das três Logias dos Almirantes da Marinha.",
            "curiosities": [
                "Permite viajar na velocidade da luz",
                "Os ataques de laser são extremamente precisos",
                "Kizaru nunca demonstrou pressa apesar de sua velocidade"
            ],
            "first_appearance": "Capítulo 507, Episódio 398",
            "destructive_power": 92,
            "defense_rating": 98,
            "speed_rating": 100,
            "image_url": "https://images.unsplash.com/photo-1680954545884-40c0c8960b85?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Velocidade", "Alta defesa"]
        },
        {
            "id": "magu-magu",
            "name": "Magu Magu no Mi",
            "japanese_name": "マグマグの実",
            "type": "Logia",
            "rarity": "Mítica",
            "power": "Magma",
            "description": "Permite criar, controlar e se transformar em magma. Superior à Mera Mera no Mi.",
            "current_user": "Sakazuki (Akainu)",
            "previous_users": [],
            "price": 4000000000,
            "available": False,
            "keywords": ["magma", "lava", "calor extremo", "queimar", "derretimento"],
            "locations": ["Marinha (Almirante da Frota)"],
            "lore": "Fruta que tornou Akainu o Almirante da Frota após derrotar Aokiji.",
            "curiosities": [
                "Matou Ace ao perfurar seu corpo",
                "É mais quente que o fogo",
                "Akainu queimou metade do rosto de Barba Branca com ela"
            ],
            "first_appearance": "Capítulo 554, Episódio 463",
            "destructive_power": 98,
            "defense_rating": 98,
            "speed_rating": 75,
            "image_url": "https://images.unsplash.com/photo-1621295538579-7fd8bb7a662a?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Alta defesa", "Controle elemental", "Combate bruto"]
        },
        {
            "id": "hie-hie",
            "name": "Hie Hie no Mi",
            "japanese_name": "ヒエヒエの実",
            "type": "Logia",
            "rarity": "Mítica",
            "power": "Gelo",
            "description": "Permite criar, controlar e se transformar em gelo.",
            "current_user": None,
            "previous_users": ["Kuzan (Aokiji)"],
            "price": 3000000000,
            "available": True,
            "keywords": ["gelo", "congelar", "frio", "congelamento", "neve"],
            "locations": ["Paradeiro desconhecido após Punk Hazard"],
            "lore": "Aokiji deixou a Marinha após perder para Akainu em Punk Hazard.",
            "curiosities": [
                "Aokiji congelou o oceano por uma semana após a batalha",
                "Perdeu uma perna na luta contra Akainu",
                "Pode congelar o tempo"
            ],
            "first_appearance": "Capítulo 319, Episódio 227",
            "destructive_power": 88,
            "defense_rating": 98,
            "speed_rating": 70,
            "image_url": "https://images.pexels.com/photos/6489573/pexels-photo-6489573.jpeg",
            "fighting_styles": ["Luta de longe", "Alta defesa", "Controle elemental"]
        },
        {
            "id": "ope-ope",
            "name": "Ope Ope no Mi",
            "japanese_name": "オペオペの実",
            "type": "Paramecia",
            "rarity": "Mítica",
            "power": "Operação",
            "description": "Permite criar uma sala onde o usuário pode manipular tudo como um cirurgião. Pode garantir imortalidade.",
            "current_user": "Trafalgar D. Water Law",
            "previous_users": [],
            "price": 5000000000,
            "available": False,
            "keywords": ["cirurgia", "cortar", "teleporte", "imortalidade", "sala"],
            "locations": ["Heart Pirates"],
            "lore": "Considerada a Akuma no Mi suprema. O Governo Mundial pagou 5 bilhões de berries por ela.",
            "curiosities": [
                "Pode conceder imortalidade ao custo da vida do usuário",
                "Law pode trocar personalidades entre corpos",
                "A cirurgia da imortalidade foi o motivo de Doflamingo querer Law na tripulação"
            ],
            "first_appearance": "Capítulo 504, Episódio 398",
            "destructive_power": 85,
            "defense_rating": 70,
            "speed_rating": 88,
            "image_url": "https://images.pexels.com/photos/6430112/pexels-photo-6430112.jpeg",
            "fighting_styles": ["Luta de longe", "Velocidade", "Melhor mobilidade"]
        },
        {
            "id": "suna-suna",
            "name": "Suna Suna no Mi",
            "japanese_name": "スナスナの実",
            "type": "Logia",
            "rarity": "Muito Rara",
            "power": "Areia",
            "description": "Permite criar, controlar e se transformar em areia.",
            "current_user": "Crocodile",
            "previous_users": [],
            "price": 1500000000,
            "available": False,
            "keywords": ["areia", "deserto", "secar", "desidratação", "tempestade de areia"],
            "locations": ["Alabasta, Impel Down, Cross Guild"],
            "lore": "Crocodile usou essa fruta para quase conquistar Alabasta.",
            "curiosities": [
                "Pode secar qualquer coisa ao tocar",
                "Fraca contra água e líquidos",
                "Crocodile criou tempestades de areia massivas"
            ],
            "first_appearance": "Capítulo 170, Episódio 103",
            "destructive_power": 82,
            "defense_rating": 95,
            "speed_rating": 78,
            "image_url": "https://images.unsplash.com/photo-1705927450843-3c1abe9b17d6?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Alta defesa", "Controle elemental"]
        },
        {
            "id": "goro-goro",
            "name": "Goro Goro no Mi",
            "japanese_name": "ゴロゴロの実",
            "type": "Logia",
            "rarity": "Mítica",
            "power": "Raio",
            "description": "Permite criar, controlar e se transformar em eletricidade.",
            "current_user": "Enel",
            "previous_users": [],
            "price": 3000000000,
            "available": False,
            "keywords": ["raio", "eletricidade", "trovão", "relâmpago", "voltagem"],
            "locations": ["Lua (Fairy Vearth)"],
            "lore": "Uma das Logias mais poderosas. Enel se considera um deus.",
            "curiosities": [
                "Permite viajar na velocidade da eletricidade",
                "Enel pode reiniciar seu próprio coração",
                "Inútil contra borracha"
            ],
            "first_appearance": "Capítulo 254, Episódio 167",
            "destructive_power": 96,
            "defense_rating": 98,
            "speed_rating": 98,
            "image_url": "https://images.unsplash.com/photo-1657625945947-2b10c313a2d1?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Velocidade", "Alta defesa", "Controle elemental"]
        },
        {
            "id": "mochi-mochi",
            "name": "Mochi Mochi no Mi",
            "japanese_name": "モチモチの実",
            "type": "Paramecia",
            "rarity": "Muito Rara",
            "power": "Mochi",
            "description": "Permite criar, controlar e se transformar em mochi. Paramecia especial que age como Logia.",
            "current_user": "Charlotte Katakuri",
            "previous_users": [],
            "price": 2000000000,
            "available": False,
            "keywords": ["mochi", "pegajoso", "elástico", "expandir", "grudar"],
            "locations": ["Whole Cake Island"],
            "lore": "Katakuri despertou sua fruta, tornando-a extremamente versátil.",
            "curiosities": [
                "Paramecia especial com propriedades de Logia",
                "Katakuri tem Haki de Observação do futuro",
                "O mochi pode grudar e aprisionar inimigos"
            ],
            "first_appearance": "Capítulo 863, Episódio 833",
            "destructive_power": 88,
            "defense_rating": 92,
            "speed_rating": 85,
            "image_url": "https://images.unsplash.com/photo-1705246535209-8c53b6b4f818?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Combate bruto", "Alta defesa", "Melhor mobilidade"]
        },
        {
            "id": "hana-hana",
            "name": "Hana Hana no Mi",
            "japanese_name": "ハナハナの実",
            "type": "Paramecia",
            "rarity": "Rara",
            "power": "Florescer",
            "description": "Permite fazer partes do corpo florescerem em qualquer superfície.",
            "current_user": "Nico Robin",
            "previous_users": [],
            "price": 500000000,
            "available": False,
            "keywords": ["florescer", "brotar", "múltiplas mãos", "membros", "espionagem"],
            "locations": ["Bando do Chapéu de Palha"],
            "lore": "Robin comeu a fruta aos 8 anos e foi caçada pelo Governo Mundial desde então.",
            "curiosities": [
                "Pode criar milhares de membros simultaneamente",
                "Robin pode criar clones completos de si mesma",
                "Extremamente versátil para espionagem"
            ],
            "first_appearance": "Capítulo 114, Episódio 67",
            "destructive_power": 70,
            "defense_rating": 55,
            "speed_rating": 75,
            "image_url": "https://images.unsplash.com/photo-1705246535209-8c53b6b4f818?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Melhor mobilidade"]
        },
        {
            "id": "bari-bari",
            "name": "Bari Bari no Mi",
            "japanese_name": "バリバリの実",
            "type": "Paramecia",
            "rarity": "Muito Rara",
            "power": "Barreira",
            "description": "Permite criar barreiras indestrutíveis.",
            "current_user": "Bartolomeo",
            "previous_users": [],
            "price": 800000000,
            "available": False,
            "keywords": ["barreira", "proteção", "defesa", "escudo", "indestrutível"],
            "locations": ["Barto Club"],
            "lore": "Bartolomeo usa suas barreiras de forma criativa em combate.",
            "curiosities": [
                "As barreiras são completamente indestrutíveis",
                "Pode criar escadas de barreiras",
                "Bartolomeo é fã número 1 de Luffy"
            ],
            "first_appearance": "Capítulo 706, Episódio 635",
            "destructive_power": 60,
            "defense_rating": 100,
            "speed_rating": 65,
            "image_url": "https://images.unsplash.com/photo-1600788894044-fb8c7d5d9442?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Alta defesa"]
        },
        {
            "id": "hobi-hobi",
            "name": "Hobi Hobi no Mi",
            "japanese_name": "ホビホビの実",
            "type": "Paramecia",
            "rarity": "Mítica",
            "power": "Brinquedo",
            "description": "Permite transformar pessoas em brinquedos e apagar suas memórias. Concede juventude eterna.",
            "current_user": "Sugar",
            "previous_users": [],
            "price": 2500000000,
            "available": False,
            "keywords": ["brinquedo", "transformação", "memória", "contrato", "juventude"],
            "locations": ["Família Donquixote"],
            "lore": "Uma das frutas mais perigosas devido ao seu efeito de apagar memórias.",
            "curiosities": [
                "Sugar parou de envelhecer aos 10 anos",
                "As pessoas esquecem completamente da existência transformada",
                "Se Sugar desmaiar, todos voltam ao normal"
            ],
            "first_appearance": "Capítulo 703, Episódio 632",
            "destructive_power": 95,
            "defense_rating": 30,
            "speed_rating": 50,
            "image_url": "https://images.unsplash.com/photo-1583487488041-5ebf7dec1db5?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe"]
        },
        {
            "id": "zou-zou",
            "name": "Zou Zou no Mi",
            "japanese_name": "ゾウゾウの実",
            "type": "Zoan",
            "rarity": "Comum",
            "power": "Elefante",
            "description": "Permite se transformar em um elefante.",
            "current_user": "Funkfreed (Espada)",
            "previous_users": [],
            "price": 100000000,
            "available": False,
            "keywords": ["elefante", "força", "grande", "mamífero", "transformação"],
            "locations": ["Spandam (CP0)"],
            "lore": "Fruta que foi dada a uma espada, criando Funkfreed.",
            "curiosities": [
                "Objetos inanimados podem comer Zoans",
                "Funkfreed pode se transformar em espada-elefante híbrida",
                "Uma das poucas Zoans comuns mostradas"
            ],
            "first_appearance": "Capítulo 400, Episódio 285",
            "destructive_power": 70,
            "defense_rating": 75,
            "speed_rating": 45,
            "image_url": "https://images.unsplash.com/photo-1588613000171-55fe9ac1e10b?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Combate bruto", "Alta defesa"]
        },
        {
            "id": "tori-tori-phoenix",
            "name": "Tori Tori no Mi, Modelo: Phoenix",
            "japanese_name": "トリトリの実 モデル：不死鳥",
            "type": "Zoan",
            "rarity": "Mítica",
            "power": "Fênix",
            "description": "Permite se transformar em uma fênix. Zoan Mítica com chamas azuis de regeneração.",
            "current_user": "Marco",
            "previous_users": [],
            "price": 3500000000,
            "available": False,
            "keywords": ["fênix", "regeneração", "voar", "chamas azuis", "cura"],
            "locations": ["Antigos Piratas do Barba Branca"],
            "lore": "Marco foi o primeiro comandante dos Piratas do Barba Branca.",
            "curiosities": [
                "As chamas azuis permitem regeneração de ferimentos",
                "Pode voar indefinidamente",
                "Uma das Zoans Míticas mais raras"
            ],
            "first_appearance": "Capítulo 554, Episódio 463",
            "destructive_power": 85,
            "defense_rating": 95,
            "speed_rating": 90,
            "image_url": "https://images.unsplash.com/photo-1680954545884-40c0c8960b85?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Velocidade", "Alta defesa", "Melhor mobilidade"]
        },
        {
            "id": "ito-ito",
            "name": "Ito Ito no Mi",
            "japanese_name": "イトイトの実",
            "type": "Paramecia",
            "rarity": "Muito Rara",
            "power": "Fio",
            "description": "Permite criar e manipular fios extremamente afiados e versáteis.",
            "current_user": null,
            "previous_users": ["Donquixote Doflamingo"],
            "price": 1500000000,
            "available": True,
            "keywords": ["fio", "cortar", "controle", "manipulação", "marionete"],
            "locations": ["Impel Down (Doflamingo preso)"],
            "lore": "Doflamingo despertou sua fruta, transformando o ambiente em fios.",
            "curiosities": [
                "Pode controlar pessoas como marionetes",
                "Os fios são mais afiados que lâminas",
                "Doflamingo criou uma gaiola de fios que cortava tudo"
            ],
            "first_appearance": "Capítulo 231, Episódio 151",
            "destructive_power": 88,
            "defense_rating": 75,
            "speed_rating": 82,
            "image_url": "https://images.unsplash.com/photo-1600788894044-fb8c7d5d9442?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Melhor mobilidade"]
        },
        {
            "id": "nikyu-nikyu",
            "name": "Nikyu Nikyu no Mi",
            "japanese_name": "ニキュニキュの実",
            "type": "Paramecia",
            "rarity": "Mítica",
            "power": "Almofada",
            "description": "Permite repelir qualquer coisa, incluindo ar, ataques e até dor.",
            "current_user": "Bartholomew Kuma",
            "previous_users": [],
            "price": 2500000000,
            "available": False,
            "keywords": ["repelir", "teleporte", "dor", "almofada", "pata"],
            "locations": ["Marinha (Pacifista)"],
            "lore": "Kuma se tornou um Pacifista para proteger o navio dos Chapéus de Palha.",
            "curiosities": [
                "Pode teletransportar pessoas para qualquer lugar do mundo",
                "Kuma pode extrair a dor de alguém",
                "Usado para criar as bombas de ar mais poderosas"
            ],
            "first_appearance": "Capítulo 234, Episódio 151",
            "destructive_power": 90,
            "defense_rating": 88,
            "speed_rating": 95,
            "image_url": "https://images.unsplash.com/photo-1705246535209-8c53b6b4f818?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Velocidade", "Alta defesa"]
        },
        {
            "id": "hito-hito-daibutsu",
            "name": "Hito Hito no Mi, Modelo: Daibutsu",
            "japanese_name": "ヒトヒトの実 モデル：大仏",
            "type": "Zoan",
            "rarity": "Mítica",
            "power": "Grande Buda",
            "description": "Permite se transformar em um Grande Buda dourado com ondas de choque.",
            "current_user": "Sengoku",
            "previous_users": [],
            "price": 2800000000,
            "available": False,
            "keywords": ["buda", "dourado", "onda de choque", "gigante", "sabedoria"],
            "locations": ["Marinha (Aposentado)"],
            "lore": "Sengoku foi o Almirante da Frota antes de Akainu.",
            "curiosities": [
                "Combina força física com ondas de choque",
                "A forma de Buda é dourada e imponente",
                "Sengoku parou Garp de atacar Akainu em Marineford"
            ],
            "first_appearance": "Capítulo 585, Episódio 497",
            "destructive_power": 92,
            "defense_rating": 90,
            "speed_rating": 70,
            "image_url": "https://images.unsplash.com/photo-1680954545884-40c0c8960b85?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Combate bruto", "Alta defesa"]
        },
        {
            "id": "doku-doku",
            "name": "Doku Doku no Mi",
            "japanese_name": "ドクドクの実",
            "type": "Paramecia",
            "rarity": "Muito Rara",
            "power": "Veneno",
            "description": "Permite criar e manipular todo tipo de veneno.",
            "current_user": "Magellan",
            "previous_users": [],
            "price": 1200000000,
            "available": False,
            "keywords": ["veneno", "tóxico", "corrosão", "morte", "envenenar"],
            "locations": ["Impel Down"],
            "lore": "Magellan é praticamente invencível dentro de Impel Down.",
            "curiosities": [
                "O veneno pode derreter pedra",
                "Magellan sofre de diarréia crônica",
                "Criou o Kinjite, veneno que causa morte lenta e dolorosa"
            ],
            "first_appearance": "Capítulo 528, Episódio 425",
            "destructive_power": 90,
            "defense_rating": 70,
            "speed_rating": 65,
            "image_url": "https://images.unsplash.com/photo-1657625945947-2b10c313a2d1?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Alta defesa"]
        },
        {
            "id": "mera-magu",
            "name": "Suna Suna no Mi",
            "japanese_name": "スナスナの実",
            "type": "Logia",
            "rarity": "Muito Rara",
            "power": "Areia",
            "description": "Permite criar, controlar e se transformar em areia.",
            "current_user": "Crocodile",
            "previous_users": [],
            "price": 1500000000,
            "available": False,
            "keywords": ["areia", "deserto", "secar"],
            "locations": ["Cross Guild"],
            "lore": "Uma das primeiras Logias introduzidas na série.",
            "curiosities": [
                "Pode absorver umidade",
                "Vulnerável à água",
                "Crocodile quase conquistou Alabasta"
            ],
            "first_appearance": "Capítulo 170",
            "destructive_power": 82,
            "defense_rating": 95,
            "speed_rating": 78,
            "image_url": "https://images.unsplash.com/photo-1621295538579-7fd8bb7a662a?crop=entropy&cs=srgb&fm=jpg&q=85",
            "fighting_styles": ["Luta de longe", "Controle elemental"]
        }
    ]
    
    await db.devil_fruits.insert_many(fruits_data)
    return {"message": "Database initialized successfully", "count": len(fruits_data)}

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()