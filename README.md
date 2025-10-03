# 🚀 Sonda em Marte - API de Controle

API REST desenvolvida como solução para o Desafio Técnico Python da RD Station. O projeto permite controlar o movimento de sondas de exploração em um planalto retangular em Marte através de comandos simples.

## ✨ Features

- ✅ **Lançamento de Sondas**: Posicione sondas em coordenadas específicas do planalto
- ✅ **Controle de Movimento**: Execute comandos de rotação (`L`, `R`) e movimentação (`M`)
- ✅ **Validação de Limites**: Impede movimentos fora dos limites da malha
- ✅ **Múltiplas Sondas**: Gerencie várias sondas simultaneamente
- ✅ **Documentação Interativa**: Interface Swagger UI para testar a API
- ✅ **Arquitetura Limpa**: Código organizado seguindo SOLID e Design Patterns

## 🏛️ Arquitetura e Design

A aplicação utiliza **Arquitetura em Camadas** com separação clara de responsabilidades:

## 📦 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passos de Instalação

1. **Clone o repositório**
```bash
git clone <URL_DO_REPOSITORIO>
cd sonda-marte-api
```

2. **Crie um ambiente virtual**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### Arquivo requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pytest==7.4.3
httpx==0.25.1
```

## 🚀 Inicialização

### Modo Desenvolvimento

Para iniciar o servidor em modo de desenvolvimento com reload automático:

```bash
uvicorn main:app --reload
```

### Modo Produção

Para ambiente de produção:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Variáveis de Ambiente (Opcional)

```bash
# Configurar porta
export PORT=8000

# Modo debug
export DEBUG=True
```

Após inicializar, a API estará disponível em:
- **URL Base**: `http://127.0.0.1:8000`
- **Documentação**: `http://127.0.0.1:8000/docs`

## 📚 Documentação da API (Swagger)

A API possui documentação interativa automática através do Swagger UI.

### Acessando o Swagger

Com o servidor rodando, acesse:

```
http://127.0.0.1:8000/docs
```

### Funcionalidades do Swagger

- 📖 Visualização completa de todos os endpoints
- 🔧 Interface interativa para testar requisições
- 📝 Schemas detalhados de request/response
- ✅ Validação em tempo real
- 📋 Exemplos de uso para cada endpoint

### Documentação Alternativa (ReDoc)

Também disponível em:

```
http://127.0.0.1:8000/redoc
```

## 🛣️ Rotas e Endpoints

### Base URL
```
http://127.0.0.1:8000/api
```

### Endpoints Disponíveis

#### 1. Lançar Nova Sonda
```http
POST /api/probes
```

**Request Body:**
```json
{
  "x": 5,
  "y": 5,
  "direction": "NORTH"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid-da-sonda",
  "x": 5,
  "y": 5,
  "direction": "NORTH"
}
```

**Parâmetros:**
- `x` (integer): Coordenada X da malha (limite superior)
- `y` (integer): Coordenada Y da malha (limite superior)
- `direction` (string): Direção inicial - `NORTH`, `SOUTH`, `EAST` ou `WEST`

---

#### 2. Mover Sonda
```http
POST /api/probes/{probe_id}/move
```

**Request Body:**
```json
{
  "commands": "LMLMLMLMM"
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-da-sonda",
  "x": 1,
  "y": 3,
  "direction": "NORTH"
}
```

**Comandos Disponíveis:**
- `L` - Rotaciona 90° para a esquerda
- `R` - Rotaciona 90° para a direita
- `M` - Move uma unidade para frente na direção atual

---

#### 3. Listar Todas as Sondas
```http
GET /api/probes
```

**Response:** `200 OK`
```json
[
  {
    "id": "uuid-1",
    "x": 1,
    "y": 3,
    "direction": "NORTH"
  },
  {
    "id": "uuid-2",
    "x": 5,
    "y": 1,
    "direction": "EAST"
  }
]
```

---

#### 4. Obter Sonda Específica
```http
GET /api/probes/{probe_id}
```

**Response:** `200 OK`
```json
{
  "id": "uuid-da-sonda",
  "x": 3,
  "y": 3,
  "direction": "EAST"
}
```

---
## 💡 Exemplos de Uso

### Exemplo Completo com cURL

```bash
# 1. Criar uma nova sonda na posição (5,5) apontando para o Norte
curl -X POST "http://127.0.0.1:8000/api/probes" \
  -H "Content-Type: application/json" \
  -d '{
    "x": 5,
    "y": 5,
    "direction": "NORTH"
  }'

# Resposta: {"id": "abc-123", "x": 5, "y": 5, "direction": "NORTH"}

# 2. Mover a sonda (substitua abc-123 pelo ID real)
curl -X POST "http://127.0.0.1:8000/api/probes/abc-123/move" \
  -H "Content-Type: application/json" \
  -d '{
    "commands": "LMLMLMLMM"
  }'

# Resposta: {"id": "abc-123", "x": 1, "y": 3, "direction": "NORTH"}

# 3. Listar todas as sondas
curl -X GET "http://127.0.0.1:8000/api/probes"

# 4. Obter uma sonda específica
curl -X GET "http://127.0.0.1:8000/api/probes/abc-123"
```

### Exemplo com Python (requests)

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Criar sonda
response = requests.post(
    f"{BASE_URL}/probes",
    json={"x": 5, "y": 5, "direction": "NORTH"}
)
probe = response.json()
probe_id = probe["id"]

# Mover sonda
response = requests.post(
    f"{BASE_URL}/probes/{probe_id}/move",
    json={"commands": "MMRMMRMRRM"}
)
print(response.json())
```

### Cenário de Teste do Desafio

```bash
# Malha 5x5, Sonda 1: (1,2,N) -> LMLMLMLMM = (1,3,N)
curl -X POST "http://127.0.0.1:8000/api/probes" \
  -H "Content-Type: application/json" \
  -d '{"x": 5, "y": 5, "direction": "NORTH"}'

# Mover para (1,2) e depois executar comandos
# (implementação depende da sua lógica de posicionamento inicial)
```

## ✅ Testes

### Executar Todos os Testes

```bash
pytest
```