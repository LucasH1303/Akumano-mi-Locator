# 📚 GUIA COMPLETO: Como Atualizar Informações das Akuma no Mi

## 🔍 Por que suas alterações no server.py não funcionavam?

Quando você editava o arquivo `backend/server.py` na linha 201, as mudanças não apareciam no site porque:

1. **Os dados já estão salvos no MongoDB** (banco de dados)
2. **O código no server.py só INICIALIZA o banco** quando ele está vazio
3. **A função `init_database()`** verifica se já existem dados e **não executa** se o banco já tiver frutas
4. **Os endpoints da API leem do MongoDB**, não do código Python

### Analogia:
Imagine que o código no `server.py` é como uma "receita" para criar frutas pela primeira vez. Uma vez que as frutas foram criadas e colocadas no banco de dados (como uma geladeira), modificar a receita não altera as frutas que já estão guardadas!

---

## ✅ SOLUÇÕES: 3 Formas de Atualizar Frutas

### **MÉTODO 1: Usando o Script Python (MAIS FÁCIL)** ⭐

#### Para atualizar APENAS a Gomu Gomu no Mi:

```bash
cd /app/backend
python update_gomu_gomu.py
```

Este script já está configurado para fazer exatamente o que você pediu:
- Tipo: Zoan
- Preço: 10 bilhões de berries
- Todas as estatísticas: 100/100

#### Para atualizar QUALQUER fruta:

1. **Abra o arquivo** `backend/update_fruit.py`

2. **Modifique estas linhas** (linhas 22-35):
```python
# ID da fruta que você quer atualizar
FRUIT_ID = "mera-mera"  # ← Troque pelo ID da fruta desejada

# Campos que você quer atualizar
updates = {
    "type": "Logia",           # Troque o tipo
    "price": 500000000,        # Troque o preço
    "destructive_power": 95,   # Troque as estatísticas
    "defense_rating": 90,
    "speed_rating": 85,
}
```

3. **Execute o script**:
```bash
cd /app/backend
python update_fruit.py
```

#### **Lista de IDs das Frutas Disponíveis:**
- `gomu-gomu` - Gomu Gomu no Mi (Luffy)
- `mera-mera` - Mera Mera no Mi (Sabo/Ace)
- `yami-yami` - Yami Yami no Mi (Barba Negra)
- `gura-gura` - Gura Gura no Mi (Barba Branca/Barba Negra)
- `pika-pika` - Pika Pika no Mi (Kizaru)
- `magu-magu` - Magu Magu no Mi (Akainu)
- `hie-hie` - Hie Hie no Mi (Aokiji)
- `ope-ope` - Ope Ope no Mi (Law)
- `suna-suna` - Suna Suna no Mi (Crocodile)
- `goro-goro` - Goro Goro no Mi (Enel)
- `mochi-mochi` - Mochi Mochi no Mi (Katakuri)
- `hana-hana` - Hana Hana no Mi (Robin)
- `bari-bari` - Bari Bari no Mi (Bartolomeo)
- `hobi-hobi` - Hobi Hobi no Mi (Sugar)
- `zou-zou` - Zou Zou no Mi (Funkfreed)
- `tori-tori-phoenix` - Tori Tori no Mi, Modelo: Phoenix (Marco)
- `ito-ito` - Ito Ito no Mi (Doflamingo)
- `nikyu-nikyu` - Nikyu Nikyu no Mi (Kuma)
- `hito-hito-daibutsu` - Hito Hito no Mi, Modelo: Daibutsu (Sengoku)
- `doku-doku` - Doku Doku no Mi (Magellan)

---

### **MÉTODO 2: Usando a API REST (Para programadores)**

Agora seu backend tem um novo endpoint para atualizar frutas!

#### Atualização Parcial (PATCH):
```bash
curl -X PATCH http://localhost:8001/api/fruits/gomu-gomu \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Zoan",
    "price": 10000000000,
    "destructive_power": 100,
    "defense_rating": 100,
    "speed_rating": 100
  }'
```

#### Atualização Completa (PUT):
```bash
curl -X PUT http://localhost:8001/api/fruits/gomu-gomu \
  -H "Content-Type: application/json" \
  -d '{
    "id": "gomu-gomu",
    "name": "Gomu Gomu no Mi",
    "japanese_name": "ゴムゴムの実",
    "type": "Zoan",
    "rarity": "Única",
    "power": "Borracha",
    "description": "Transforma o corpo em borracha. Verdadeiro nome: Hito Hito no Mi, Modelo: Nika.",
    "current_user": "Monkey D. Luffy",
    "previous_users": ["Joy Boy"],
    "price": 10000000000,
    "available": false,
    "keywords": ["borracha", "elástico", "esticar", "flexível", "nika"],
    "locations": ["East Blue (roubada por Shanks)"],
    "lore": "Fruta lendária guardada pelo Governo Mundial por 800 anos.",
    "curiosities": [
        "O Governo Mundial tentou capturá-la por séculos",
        "Despertada, permite transformar o ambiente em borracha",
        "É considerada a fruta mais ridícula do mundo"
    ],
    "first_appearance": "Capítulo 1, Episódio 4",
    "destructive_power": 100,
    "defense_rating": 100,
    "speed_rating": 100,
    "image_url": "https://images.unsplash.com/photo-1583487488041-5ebf7dec1db5?crop=entropy&cs=srgb&fm=jpg&q=85",
    "fighting_styles": ["Combate bruto", "Velocidade", "Melhor mobilidade"]
  }'
```

---

### **MÉTODO 3: Modificando Diretamente no MongoDB**

Se você tiver acesso ao MongoDB Compass ou mongo shell:

```javascript
use test_database

db.devil_fruits.updateOne(
  { "id": "gomu-gomu" },
  { 
    $set: {
      "type": "Zoan",
      "price": 10000000000,
      "destructive_power": 100,
      "defense_rating": 100,
      "speed_rating": 100
    }
  }
)
```

---

## 📝 CAMPOS QUE VOCÊ PODE MODIFICAR

Aqui está a lista completa de campos que você pode alterar:

```python
{
    "id": "string",                    # ID único (não altere!)
    "name": "string",                  # Nome em português
    "japanese_name": "string",         # Nome em japonês
    "type": "string",                  # Paramecia, Logia ou Zoan
    "rarity": "string",                # Comum, Rara, Muito Rara, Mítica, Única
    "power": "string",                 # Poder principal
    "description": "string",           # Descrição detalhada
    "current_user": "string ou null",  # Usuário atual
    "previous_users": ["lista"],       # Lista de usuários anteriores
    "price": 123456789,                # Preço em berries (número)
    "available": true/false,           # Se está disponível
    "keywords": ["lista"],             # Palavras-chave para busca
    "locations": ["lista"],            # Localizações conhecidas
    "lore": "string",                  # História da fruta
    "curiosities": ["lista"],          # Curiosidades
    "first_appearance": "string",      # Primeira aparição
    "destructive_power": 0-100,        # Poder destrutivo (0-100)
    "defense_rating": 0-100,           # Defesa (0-100)
    "speed_rating": 0-100,             # Velocidade (0-100)
    "image_url": "string",             # URL da imagem
    "fighting_styles": ["lista"]       # Estilos de luta
}
```

---

## 🎯 EXEMPLO PRÁTICO: Passo a Passo Completo

### Vamos atualizar a Mera Mera no Mi para ter estatísticas máximas:

1. **Abra o arquivo** `backend/update_fruit.py`

2. **Modifique as linhas 22-35:**
```python
FRUIT_ID = "mera-mera"  # ← Mera Mera no Mi

updates = {
    "destructive_power": 100,  # De 95 para 100
    "defense_rating": 100,     # De 98 para 100
    "speed_rating": 100,       # De 85 para 100
    "price": 1000000000        # 1 bilhão de berries
}
```

3. **Execute:**
```bash
cd /app/backend
python update_fruit.py
```

4. **Verifique no site:**
   - Vá para: https://devil-fruit-db.preview.emergentagent.com/encyclopedia
   - Clique em "Ver detalhes" na Mera Mera no Mi
   - As novas estatísticas devem aparecer!

---

## ⚠️ IMPORTANTE: Reiniciar vs Hot Reload

- **Alterações no banco de dados NÃO precisam** reiniciar o servidor
- **Alterações no código Python (server.py) PRECISAM** reiniciar:
  ```bash
  sudo supervisorctl restart backend
  ```

---

## 🚀 RESUMO RÁPIDO

### Para atualizar a Gomu Gomu no Mi agora:
```bash
cd /app/backend
python update_gomu_gomu.py
```

### Para atualizar outras frutas no futuro:
1. Edite `backend/update_fruit.py`
2. Mude o `FRUIT_ID` e o dicionário `updates`
3. Execute: `python update_fruit.py`

---

## ❓ PERGUNTAS FREQUENTES

**P: Por que não posso simplesmente editar o server.py?**
R: Porque os dados já estão no MongoDB. O server.py só inicializa o banco pela primeira vez.

**P: E se eu quiser resetar tudo e começar de novo?**
R: Você pode deletar todas as frutas e rodar `init_database()` novamente, mas vai perder todas as alterações.

**P: Como eu vejo qual fruta tem qual ID?**
R: Você pode acessar a URL da fruta no navegador. Exemplo: 
   `/fruit/gomu-gomu` → ID é "gomu-gomu"

**P: Posso criar frutas novas?**
R: Sim! Você pode criar um endpoint POST ou adicionar mais frutas no array `fruits_data` do `init_database()`.

---

## 📞 SUPORTE

Se você tiver dúvidas sobre como modificar outras frutas, me pergunte! Posso te ajudar com scripts específicos para cada caso.

Boa sorte com seu banco de dados de Akuma no Mi! 🍎⚡🔥
