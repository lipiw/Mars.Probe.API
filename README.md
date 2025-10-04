# Sonda em Marte - API de Controle

![Versão do Python](https://img.shields.io/badge/Python-3.9+-blue.svg)

API REST desenvolvida como solução para o lançamento de uma **Sonda em Marte**. O projeto permite controlar sondas de exploração em um planalto retangular, recebendo sequências de comandos para movimentá-las e garantindo que permaneçam dentro dos limites da área designada.

## 🏛️ Arquitetura e Decisões de Design

A aplicação foi estruturada seguindo uma **Arquitetura em Camadas (Layered Architecture)** para garantir uma clara separação de responsabilidades, facilitando os testes e a evolução do código.

-   **Camada de Apresentação (API)**: Construída com **FastAPI**, é responsável por gerenciar as rotas HTTP, validar os dados de entrada/saída com Pydantic e delegar as ações para a camada de serviço.
-   **Camada de Serviço (Service)**: Orquestra os casos de uso da aplicação. Ela atua como uma ponte entre a camada de API e a lógica de domínio, sem conter regras de negócio.
-   **Camada de Domínio (Domain)**: O núcleo da aplicação. Contém as entidades (`Probe`, `Grid`) e a lógica de negócio pura, sem dependências de frameworks ou bancos de dados.
-   **Camada de Persistência (Repository)**: Abstrai o acesso aos dados. A implementação atual é em memória, mas a arquitetura permite a fácil substituição por um banco de dados relacional ou NoSQL.

A solução foi projetada seguindo os princípios **SOLID** e utilizando os seguintes **Design Patterns**:
-   **State Pattern**: Para gerenciar a direção da sonda (`NorthState`, `EastState`, etc.), eliminando condicionais complexas e deixando o código mais limpo e aderente ao princípio Aberto/Fechado.
-   **Repository Pattern**: Para desacoplar a lógica de negócio do armazenamento de dados.
-   **Injeção de Dependência**: Utilizada extensivamente pelo FastAPI para fornecer as dependências (como o `ProbeService`) às camadas superiores de forma desacoplada, o que simplifica drasticamente os testes.

## 🛠️ Tecnologias Utilizadas

-   **Linguagem**: Python 3.12
-   **Framework Principal**: FastAPI
-   **Validação de Dados**: Pydantic
-   **Servidor ASGI**: Uvicorn
-   **Testes**: Pytest, Pytest-Mock, HTTPX (via `TestClient`)

## 🗄️ Persistência de Dados com SQLAlchemy e SQLite

Para garantir que o estado das sondas seja mantido entre as execuções, a aplicação utiliza um banco de dados para persistência.

### Tecnologia

A solução usa **SQLAlchemy**, o principal ORM (Object-Relational Mapper) do ecossistema Python, para interagir com o banco de dados de forma segura e eficiente.

### Banco de Dados

O banco de dados padrão é o **SQLite**, que armazena todas as informações em um único arquivo chamado `mars_probe.db` na raiz do projeto.

### Criação Automática

Ao iniciar a aplicação pela primeira vez, o arquivo `mars_probe.db` e as tabelas necessárias são criados automaticamente.

### Flexibilidade

Graças ao **Repository Pattern**, a troca do SQLite por outro banco de dados (como **PostgreSQL** ou **MySQL**) pode ser feita com alterações mínimas no código, sem impactar a lógica de negócio da aplicação.

## 🚀 Começando

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos
-   Python 3.9+
-   Git

### Instalação
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/lipiw/Mars.Probe.API.git](https://github.com/lipiw/Mars.Probe.API.git)
    cd Mars.Probe.API
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
### 📚 Documentação e Uso da API (Swagger UI)

A forma mais fácil de explorar e interagir com a API é através da documentação interativa **Swagger UI**, que é gerada automaticamente pelo **FastAPI**.

Com o servidor rodando, acesse a seguinte URL no seu navegador:

➡️ [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Na interface do Swagger, você poderá:

- Visualizar todos os endpoints disponíveis.
- Ver os schemas de dados para requisições e respostas.
- Executar requisições de teste diretamente pelo navegador.

Uma documentação alternativa, com foco em leitura, também está disponível em:

➡️ [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---
### Execução
Para iniciar o servidor em modo de desenvolvimento com hot-reload:
```bash
uvicorn main:app --reload
```


### 1. Comando `docker build`

Este comando lê o `Dockerfile`, executa seus passos e cria uma imagem Docker localmente.

**Execute no seu terminal, na raiz do projeto:**
```bash
docker build -t mars-probe-api .
```


### 2. Comando `docker run`

Este comando inicia um container a partir da imagem que você acabou de construir.

**Execute no seu terminal:**
```bash
docker run -d -p 8000:8000 --name mars-probe-container mars-probe-api
```

Depois de executar este comando, sua API estará rodando e acessível em `http://localhost:8000`, exatamente como quando você rodava localmente, mas agora totalmente containerizada!

Para parar o container, você pode usar:
```bash
docker stop mars-probe-container
```