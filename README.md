# 🐾 PetShop Management API

Uma API REST robusta para gerenciamento completo de PetShop, desenvolvida com FastAPI e seguindo princípios de Clean Architecture. O sistema oferece controle total de clientes, pets, agendamentos e serviços veterinários.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido para modernizar e digitalizar o gerenciamento de petshops, oferecendo uma solução completa para:

- **Gestão de Clientes**: Cadastro, atualização e controle de dados dos proprietários de pets
- **Gerenciamento de Pets**: Registro detalhado dos animais com informações sobre raça, idade e características
- **Sistema de Agendamentos**: Controle de consultas e serviços com data e horário
- **Catálogo de Serviços**: Gestão de tipos de serviços oferecidos com preços e duração
- **Autenticação Segura**: Sistema de login diferenciado para administradores e clientes
- **Controle de Acesso**: Middleware de autenticação com JWT tokens

## ✨ Funcionalidades

### 👥 Gestão de Clientes
- ✅ Cadastro de novos clientes
- ✅ Autenticação com email e senha
- ✅ Busca de clientes (apenas administradores)
- ✅ Atualização de dados (apenas administradores)
- ✅ Exclusão de contas (apenas administradores)

### 🐕 Gestão de Pets
- ✅ Cadastro de pets vinculados aos clientes
- ✅ Listagem de todos os pets do cliente
- ✅ Busca específica de pets
- ✅ Atualização de informações dos pets
- ✅ Exclusão de registros de pets

### 👨‍💼 Painel Administrativo
- ✅ Login específico para administradores
- ✅ Gerenciamento de clientes e pets

### 🔐 Segurança
- ✅ Autenticação JWT
- ✅ Hash de senhas com bcrypt
- ✅ Middleware de autorização
- ✅ Controle de acesso por perfil (Admin/Cliente)

## 🛠️ Tecnologias

### Backend
- **[Python 3.12+](https://python.org/)** - Linguagem de programação
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[SQLModel](https://sqlmodel.tiangolo.com/)** - ORM moderno baseado no SQLAlchemy
- **[PostgreSQL](https://postgresql.org/)** - Banco de dados relacional
- **[Alembic](https://alembic.sqlalchemy.org/)** - Migrations do banco de dados

### Segurança & Autenticação
- **[PyJWT](https://pyjwt.readthedocs.io/)** - Geração e validação de tokens JWT
- **[Passlib](https://passlib.readthedocs.io/)** - Hash de senhas
- **[python-decouple](https://github.com/henriquebastos/python-decouple)** - Gerenciamento de variáveis de ambiente

### Desenvolvimento & Testes
- **[Pytest](https://pytest.org/)** - Framework de testes
- **[Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)** - Suporte a testes assíncronos
- **[Pytest-mock](https://pytest-mock.readthedocs.io/)** - Mocking para testes
- **[Ruff](https://github.com/astral-sh/ruff)** - Linter e formatter
- **[Pylint](https://pylint.pycqa.org/)** - Análise estática de código

### DevOps
- **[Docker](https://docker.com/)** - Containerização
- **[Docker Compose](https://docs.docker.com/compose/)** - Orquestração de containers
- **[UV](https://github.com/astral-sh/uv)** - Gerenciador de pacotes Python ultrarrápido

## 🏗️ Arquitetura

O projeto segue os princípios da **Clean Architecture**, garantindo:

- **Separação de responsabilidades**
- **Baixo acoplamento**
- **Alta coesão**
- **Testabilidade**
- **Manutenibilidade**

### Estrutura de Pastas

```
src/
├── main/                    # Camada de apresentação
│   ├── routes/             # Definição das rotas da API
│   ├── adapters/           # Adaptadores de requisição
│   ├── composers/          # Injeção de dependências
│   └── server/            # Configuração do servidor
├── modules/               # Módulos de negócio
│   ├── authenticate_admin/ # Autenticação de administradores
│   ├── authenticate_user/  # Autenticação de usuários
│   ├── pet/               # Domínio de pets
│   ├── schedule/          # Domínio de agendamentos
│   └── user/              # Domínio de usuários
├── infra/                 # Camada de infraestrutura
│   └── db/               # Configurações do banco
│       ├── entities/     # Entidades do banco
│       └── repositories/ # Repositórios
├── drivers/              # Drivers externos
│   ├── jwt/             # Serviços JWT
│   └── password_hasher/ # Hash de senhas
├── middlewares/          # Middlewares de autenticação
├── errors/              # Tratamento de erros
└── tests/               # Testes automatizados
```

## 📋 Pré-requisitos

- **Python 3.12+**
- **Docker** e **Docker Compose**
- **Git**

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/Andremelo001/schedule-pet-shop.git
cd schedule-pet-shop
```

### 2. Configure o ambiente virtual
```bash
# Instale o UV (se ainda não tiver)
pip install uv

# Crie e ative o ambiente virtual
uv venv
uv pip sync pyproject.toml
```

### 3. Inicie o banco de dados
```bash
docker-compose up -d
```

### 4. Execute as migrations
```bash
alembic upgrade head
```

### 5. Inicie a aplicação
```bash
uv run fastapi dev src/main.py
```

A API estará disponível em: `http://localhost:8000`

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de Dados
DATABASE_URL=postgresql+asyncpg://seu_user:sua_senha@localhost:5432/nome_do_banco

# JWT
JWT_SECRET=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_TIME=30
SENHA_ADMIN="senha_admin"

# Aplicação
DEBUG=True
```

## 🏛️ Modelo de Dados

```mermaid
classDiagram
    direction LR
    class Admin {
        id: uuid
        name: str
        senha: str
        user: str
    }

    class Client {
        id: uuid 
        name: str
        cpf: str
        senha: str
        email: str
        age: int
    }

    class Pet {
        id: uuid
        name: str
        breed: str
        age: int
        size_in_centimeters: int
        id_client: uuid
    }

    class Schedule {
        id: uuid
        date_schedule: date
        id_client: uuid
        id_pet: uuid
        total_price_schedule: int
    }

    class Services {
        id: uuid
        duration_in_minutes: int
        type_service: str
        price: float
    }

    Client "1" -- "*" Pet
    Client "1" -- "*" Schedule
    Schedule "*" --> "*" Services
    Schedule "*" -- "1" Pet
``` 

## 👨‍💻 Autor

**André Melo**
- GitHub: [@Andremelo001](https://github.com/Andremelo001)
- LinkedIn: [André Melo](www.linkedin.com/in/melooandree)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório! 
