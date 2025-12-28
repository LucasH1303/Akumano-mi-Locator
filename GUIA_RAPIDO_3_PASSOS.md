# 🚀 GUIA RÁPIDO - 3 PASSOS SIMPLES

## ⚡ ATALHO ULTRA RÁPIDO

### Para atualizar QUALQUER fruta em 3 comandos:

```bash
# 1. Entre na pasta backend
cd /app/backend

# 2. Edite o arquivo (mude FRUIT_ID e updates)
nano update_fruit.py

# 3. Execute
python update_fruit.py
```

**Pronto! As mudanças aparecem no site IMEDIATAMENTE!** ✨

---

## 📝 O QUE EDITAR NO ARQUIVO

Abra `/app/backend/update_fruit.py` e modifique **APENAS ESTAS LINHAS**:

```python
# LINHA 22 - Qual fruta você quer modificar?
FRUIT_ID = "gomu-gomu"  # ← Troque pelo ID da fruta

# LINHA 26 - O que você quer mudar?
updates = {
    "type": "Zoan",            # ← Tipo da fruta
    "price": 10000000000,      # ← Preço em berries
    "destructive_power": 100,  # ← Poder (0-100)
    "defense_rating": 100,     # ← Defesa (0-100)
    "speed_rating": 100,       # ← Velocidade (0-100)
}
```

**IMPORTANTE:** Só inclua os campos que você quer mudar!

---

## 🎯 EXEMPLOS PRÁTICOS

### Exemplo 1: Aumentar o preço da Mera Mera

```python
FRUIT_ID = "mera-mera"

updates = {
    "price": 1000000000  # 1 bilhão de berries
}
```

### Exemplo 2: Deixar Yami Yami com stats máximas

```python
FRUIT_ID = "yami-yami"

updates = {
    "destructive_power": 100,
    "defense_rating": 100,
    "speed_rating": 100
}
```

### Exemplo 3: Mudar tipo da Ope Ope

```python
FRUIT_ID = "ope-ope"

updates = {
    "type": "Logia"  # De Paramecia para Logia
}
```

---

## 📋 IDs DAS FRUTAS (Copie e Cole)

### Mais Populares:
```
gomu-gomu     - Gomu Gomu no Mi (Luffy)
mera-mera     - Mera Mera no Mi (Sabo/Ace)
yami-yami     - Yami Yami no Mi (Barba Negra)
gura-gura     - Gura Gura no Mi (Barba Branca)
ope-ope       - Ope Ope no Mi (Law)
```

### Logias Poderosas:
```
pika-pika     - Pika Pika no Mi (Kizaru)
magu-magu     - Magu Magu no Mi (Akainu)
hie-hie       - Hie Hie no Mi (Aokiji)
goro-goro     - Goro Goro no Mi (Enel)
suna-suna     - Suna Suna no Mi (Crocodile)
```

### Outras:
```
mochi-mochi   - Mochi Mochi no Mi (Katakuri)
hana-hana     - Hana Hana no Mi (Robin)
bari-bari     - Bari Bari no Mi (Bartolomeo)
hobi-hobi     - Hobi Hobi no Mi (Sugar)
ito-ito       - Ito Ito no Mi (Doflamingo)
```

**Ver lista completa:**
```bash
cd /app/backend
python list_fruits.py
```

---

## 🎨 CAMPOS QUE VOCÊ PODE MODIFICAR

### Básicos:
```python
"name": "Nome da Fruta"           # Nome em português
"japanese_name": "日本語"          # Nome em japonês
"type": "Paramecia"               # Paramecia, Logia ou Zoan
"rarity": "Mítica"                # Comum, Rara, Muito Rara, Mítica, Única
"power": "Descrição do poder"     # Descrição curta
```

### Estatísticas:
```python
"price": 1000000000               # Preço em berries (número)
"destructive_power": 95           # Poder destrutivo (0-100)
"defense_rating": 90              # Defesa (0-100)
"speed_rating": 85                # Velocidade (0-100)
```

### Informações:
```python
"current_user": "Nome"            # Usuário atual
"previous_users": ["Nome1", "Nome2"]  # Usuários anteriores
"available": false                # true = disponível, false = não
"description": "Descrição longa"  # Descrição detalhada
"lore": "História da fruta"       # História/lore
```

### Avançados:
```python
"keywords": ["palavra1", "palavra2"]  # Palavras-chave para busca
"locations": ["Local1", "Local2"]     # Localizações
"curiosities": ["Fato1", "Fato2"]     # Curiosidades
"first_appearance": "Capítulo X"      # Primeira aparição
"fighting_styles": ["Estilo1"]        # Estilos de luta
"image_url": "https://..."            # URL da imagem
```

---

## 🔥 RECEITAS PRONTAS

### Deixar uma fruta SUPER PODEROSA:
```python
updates = {
    "rarity": "Única",
    "price": 10000000000,
    "destructive_power": 100,
    "defense_rating": 100,
    "speed_rating": 100
}
```

### Deixar uma fruta DISPONÍVEL:
```python
updates = {
    "available": True,
    "current_user": None
}
```

### Mudar o USUÁRIO:
```python
updates = {
    "current_user": "Novo Usuário",
    "available": False
}
```

### Aumentar PREÇO:
```python
updates = {
    "price": 5000000000  # 5 bilhões
}
```

---

## ✅ CHECKLIST ANTES DE EXECUTAR

- [ ] Abri o arquivo `update_fruit.py`
- [ ] Mudei o `FRUIT_ID` para a fruta correta
- [ ] Defini os campos em `updates`
- [ ] Salvei o arquivo (Ctrl+O no nano, depois Ctrl+X)
- [ ] Executei `python update_fruit.py`

---

## 🆘 PROBLEMAS COMUNS

### "Fruta não encontrada"
→ Verifique se o ID está correto
→ Execute `python list_fruits.py` para ver os IDs

### "Nenhuma alteração foi feita"
→ Os valores já eram iguais
→ Está tudo OK!

### "Erro de sintaxe"
→ Verifique se fechou todas as aspas e chaves
→ Exemplo correto: `"type": "Zoan",`

---

## 🎓 RESUMO EXECUTIVO

1. **Abra:** `/app/backend/update_fruit.py`
2. **Mude:** `FRUIT_ID` e `updates`
3. **Execute:** `python update_fruit.py`
4. **Pronto:** Mudanças no site IMEDIATAS!

**Não precisa reiniciar nada!** 🚀

---

## 📱 CONTATO RÁPIDO

**Quer ajuda?** Pergunte:
- "Como eu mudo o tipo da [fruta]?"
- "Como eu deixo a [fruta] mais cara?"
- "Qual é o ID da [fruta]?"

**Respondo em segundos!** 💬

---

**Última atualização:** Hoje  
**Status:** ✅ Testado e funcionando  
**Facilidade:** ⭐⭐⭐⭐⭐ (5/5)
