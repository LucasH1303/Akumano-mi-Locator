# 🍎 Devil Fruit Database - Banco de Dados de Akuma no Mi

Banco de dados completo das Akuma no Mi (Frutas do Diabo) de One Piece com sistema de busca, rankings e estatísticas detalhadas.

## 🎯 ATUALIZAÇÃO IMPORTANTE!

### ✅ Problema Resolvido: Como Atualizar Informações das Frutas

**ANTES:** Editar `backend/server.py` não funcionava ❌  
**AGORA:** Use os scripts Python para atualização direta no banco! ✅

## 🚀 GUIA RÁPIDO - Atualizar Frutas em 3 Passos

```bash
# 1. Entre na pasta backend
cd /app/backend

# 2. Edite o arquivo de atualização
nano update_fruit.py
# Mude: FRUIT_ID e updates

# 3. Execute
python update_fruit.py
```

**As mudanças aparecem IMEDIATAMENTE no site!** ✨

## 📚 Documentação Completa

### Guias Criados:
1. **`GUIA_RAPIDO_3_PASSOS.md`** ⭐ - Comece por aqui!
2. **`SOLUCAO_COMPLETA.md`** - Explicação detalhada do problema
3. **`GUIA_ATUALIZACAO_FRUTAS.md`** - Guia técnico completo
4. **`RESUMO_MUDANCAS.md`** - Lista de mudanças realizadas

### Scripts Disponíveis:
- **`backend/update_fruit.py`** - Atualiza qualquer fruta (USE ESTE!)
- **`backend/update_gomu_gomu.py`** - Atualiza Gomu Gomu no Mi
- **`backend/list_fruits.py`** - Lista todas as frutas e IDs

## 🎯 Exemplo Rápido

### Atualizar a Mera Mera no Mi:

1. Abra: `/app/backend/update_fruit.py`

2. Modifique:
```python
FRUIT_ID = "mera-mera"

updates = {
    "price": 1000000000,       # 1 bilhão de berries
    "destructive_power": 100,  # Poder máximo
}
```

3. Execute:
```bash
cd /app/backend
python update_fruit.py
```

## 📋 IDs das Frutas Mais Populares

```
gomu-gomu     - Gomu Gomu no Mi (Luffy)
mera-mera     - Mera Mera no Mi (Sabo/Ace)
yami-yami     - Yami Yami no Mi (Barba Negra)
gura-gura     - Gura Gura no Mi (Barba Branca)
ope-ope       - Ope Ope no Mi (Law)
pika-pika     - Pika Pika no Mi (Kizaru)
magu-magu     - Magu Magu no Mi (Akainu)
```

Ver lista completa: `python backend/list_fruits.py`

## 🛠️ Tecnologias

- **Backend:** FastAPI + Python
- **Frontend:** React + Tailwind CSS
- **Banco de Dados:** MongoDB
- **Deploy:** Kubernetes (Emergent Platform)

## 🌐 URLs

- **Site:** https://devil-fruit-db.preview.emergentagent.com
- **Enciclopédia:** https://devil-fruit-db.preview.emergentagent.com/encyclopedia
- **API:** https://devil-fruit-db.preview.emergentagent.com/api

## 📡 Endpoints da API

### Consulta:
- `GET /api/fruits` - Lista todas as frutas
- `GET /api/fruits/{fruit_id}` - Busca fruta específica
- `POST /api/search` - Busca avançada

### Atualização (NOVO!):
- `PUT /api/fruits/{fruit_id}` - Atualização completa
- `PATCH /api/fruits/{fruit_id}` - Atualização parcial

### Rankings:
- `GET /api/rankings/expensive` - Frutas mais caras
- `GET /api/rankings/destructive` - Frutas mais destrutivas
- `GET /api/rankings/rare` - Frutas mais raras
- `GET /api/rankings/defense` - Melhor defesa
- `GET /api/rankings/speed` - Maior velocidade

## 💡 Por que editar server.py não funciona?

**Problema:** Os dados das frutas estão no MongoDB, não no código!

```
server.py (linha 201)     →  Apenas INICIALIZA o banco (1x)
MongoDB                   →  Onde os dados REALMENTE estão
```

**Solução:** Use os scripts Python para atualizar diretamente no banco.

## ✅ Últimas Atualizações

- ✅ Gomu Gomu no Mi atualizada (Tipo: Zoan, Stats: 100/100)
- ✅ Endpoints de atualização criados
- ✅ Scripts de manutenção implementados
- ✅ Documentação completa em português

## 🆘 Suporte

**Precisa de ajuda?**
1. Leia o `GUIA_RAPIDO_3_PASSOS.md`
2. Consulte o `GUIA_ATUALIZACAO_FRUTAS.md`
3. Execute `python backend/list_fruits.py` para ver IDs

## 🎉 Status do Projeto

✅ **Funcionando perfeitamente!**

- Backend: ✅ RUNNING
- Frontend: ✅ RUNNING  
- MongoDB: ✅ RUNNING
- Atualizações: ✅ TESTADAS

---

**Desenvolvido com ❤️ para fãs de One Piece**  
**Última atualização:** 2025
