# 🐾 PetShop Management API

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Uma API REST robusta para gerenciamento completo de PetShop, desenvolvida com FastAPI e seguindo princípios de Clean Architecture. O sistema oferece controle total de clientes, pets, agendamentos e serviços veterinários, com integração a microserviços de pagamento.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
  - [Microserviços](#microserviços)
  - [Estrutura de Pastas](#estrutura-de-pastas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
  - [Opção 1: Docker (Recomendada)](#-opção-1-instalação-com-docker-recomendada)
  - [Opção 2: Instalação Local](#-opção-2-instalação-local-desenvolvimento)
- [API Endpoints](#api-endpoints)
- [Configuração](#configuração)
- [Modelo de Dados](#-modelo-de-dados)
- [Workers e Processamento Assíncrono](#-workers-e-processamento-assíncrono)
- [Validações de Negócio](#-validações-de-negócio)
- [Testes](#-testes)
- [Recursos Adicionais](#-recursos-adicionais)
- [Autor](#-autor)

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido para modernizar e digitalizar o gerenciamento de petshops, oferecendo uma solução completa e escalável baseada em arquitetura de microserviços para:

- **Gestão de Clientes**: Cadastro, atualização e controle de dados dos proprietários de pets com autenticação segura
- **Gerenciamento de Pets**: Registro detalhado dos animais com informações sobre raça, idade e características físicas
- **Sistema de Agendamentos Inteligente**: 
  - Controle de consultas e serviços com validação automática de conflitos
  - Sugestão de horários disponíveis em tempo real
  - Validações robustas de horário comercial e dias úteis
  - Cálculo automático de duração e preço total
- **Pagamento dos Agendamentos**: 
  - Cliente pode realizar o pagamento de seus respectivos agendamentos via Pix
  - Integração com microserviço dedicado de pagamentos
  - Processamento assíncrono de eventos de pagamento via RabbitMQ
  - Atualização automática de status após confirmação
- **Catálogo de Serviços**: Gestão de tipos de serviços oferecidos com preços e duração
- **Autenticação Segura**: Sistema de login diferenciado para administradores e clientes com JWT
- **Controle de Acesso**: Middleware de autenticação com múltiplos níveis de permissão
- **Notificações por Email**: Sistema automático de envio de emails para cancelamentos

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

### 🗓️ Sistema de Agendamentos
- ✅ Criação de agendamentos com múltiplos serviços
- ✅ Validação de conflitos de horário (detecção de sobreposição)
- ✅ Sugestão inteligente de horários disponíveis
- ✅ Limitação de até 3 serviços por agendamento
- ✅ Controle de duração máxima (120 minutos)
- ✅ Validação de dias úteis (não funciona aos domingos)
- ✅ Validação de horários comerciais (8h-12h e 14h-18h)
- ✅ Apenas horários cheios são aceitos (sem minutos quebrados)
- ✅ Validação de pet vinculado ao cliente
- ✅ Cálculo automático do preço total do agendamento
- ✅ Listagem de agendamentos (administradores)
- ✅ Visualização de agendamentos ativos
- ✅ Cancelamento de agendamentos com notificação por email
- ✅ Solicitação de cancelamento com token JWT específico
- ✅ Exclusão de agendamentos (com validação de data)

### 💳 Sistema de Pagamentos (Microserviço)
- ✅ Geração de pagamentos via Pix para agendamentos
- ✅ Integração com microserviço de pagamentos externo
- ✅ Arquitetura de microserviços para processamento de pagamentos
- ✅ Isolamento de responsabilidades com PaymentGatewayService
- ✅ Comunicação assíncrona via HTTP com timeout configurável
- ✅ Consulta de status de pagamento por agendamento
- ✅ Processamento de eventos de pagamento via RabbitMQ
- ✅ Worker dedicado para consumir eventos de pagamento
- ✅ Atualização automática de status do agendamento após pagamento
- ✅ Validação para evitar pagamentos duplicados
- ✅ Tratamento robusto de erros e timeouts
- ✅ Garantia de mensagens com ACK/NACK no RabbitMQ

### 🛠️ Gestão de Serviços
- ✅ Cadastro de novos tipos de serviços
- ✅ Definição de duração e preços dos serviços
- ✅ Listagem de todos os serviços disponíveis
- ✅ Atualização de serviços (com validação de agendamentos)
- ✅ Exclusão de serviços (com proteção contra agendamentos ativos)
- ✅ Relacionamento muitos-para-muitos com agendamentos

### 📧 Sistema de Notificações
- ✅ Envio de emails automáticos para cancelamento
- ✅ Configuração SMTP para envio de emails
- ✅ Templates personalizados para notificações
- ✅ Notificação apenas para o cliente proprietário

### 🔐 Segurança
- ✅ Autenticação JWT diferenciada (Admin/Cliente)
- ✅ Hash de senhas com bcrypt
- ✅ Middleware de autorização por perfil
- ✅ Tokens específicos para cancelamento
- ✅ Validação de permissões por endpoint
- ✅ Proteção de rotas sensíveis

## 🛠️ Tecnologias

### Backend
- **[Python 3.12+](https://python.org/)** - Linguagem de programação
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[SQLModel](https://sqlmodel.tiangolo.com/)** - ORM moderno baseado no SQLAlchemy
- **[PostgreSQL](https://postgresql.org/)** - Banco de dados relacional
- **[Alembic](https://alembic.sqlalchemy.org/)** - Migrations do banco de dados
- **[RabbitMQ](https://www.rabbitmq.com/)** - Sistema de mensageria para comunicação assíncrona
- **[Pika](https://pika.readthedocs.io/)** - Cliente Python para RabbitMQ

### Segurança & Autenticação
- **[PyJWT](https://pyjwt.readthedocs.io/)** - Geração e validação de tokens JWT
- **[Passlib](https://passlib.readthedocs.io/)** - Hash de senhas
- **[python-decouple](https://github.com/henriquebastos/python-decouple)** - Gerenciamento de variáveis de ambiente

### Comunicação
- **[SMTP](https://docs.python.org/3/library/smtplib.html)** - Envio de emails para notificações
- **[SSL](https://docs.python.org/3/library/ssl.html)** - Conexões seguras para email
- **[HTTPX](https://www.python-httpx.org/)** - Cliente HTTP assíncrono para comunicação entre microserviços

### Desenvolvimento & Testes
- **[Pytest](https://pytest.org/)** - Framework de testes
- **[Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)** - Suporte a testes assíncronos
- **[Pytest-mock](https://pytest-mock.readthedocs.io/)** - Mocking para testes
- **[Ruff](https://github.com/astral-sh/ruff)** - Linter e formatter ultrarrápido
- **[Pylint](https://pylint.pycqa.org/)** - Análise estática de código

### DevOps
- **[Docker](https://docker.com/)** - Containerização
- **[Docker Compose](https://docs.docker.com/compose/)** - Orquestração de containers
- **[UV](https://github.com/astral-sh/uv)** - Gerenciador de pacotes Python ultra-rápido

## 🏗️ Arquitetura

O projeto segue os princípios da **Clean Architecture** e **Arquitetura de Microserviços**, garantindo:

- **Separação de responsabilidades**
- **Baixo acoplamento**
- **Alta coesão**
- **Testabilidade**
- **Manutenibilidade**
- **Escalabilidade independente de serviços**

### Microserviços

Este sistema é composto por múltiplos microserviços que trabalham de forma integrada:

#### 🏪 **PetShop Management API** (Este repositório)
Serviço principal responsável por:
- Gestão de clientes, pets e agendamentos
- Catálogo de serviços
- Autenticação e autorização
- Coordenação de pagamentos
- Consumo de eventos de pagamento via RabbitMQ

#### 💰 **[Payments API](https://github.com/Andremelo001/payments_API)**
Microserviço dedicado ao processamento de pagamentos:
- Geração de pagamentos via Pix
- Processamento de transações
- Integração com gateways de pagamento
- Gestão de status de pagamentos
- Publicação de eventos de pagamento via RabbitMQ

> **Arquitetura de Microserviços**: A comunicação entre os serviços é feita de forma híbrida:
> - **Síncrona via HTTP**: Para operações de consulta e criação de pagamentos
> - **Assíncrona via RabbitMQ**: Para notificações de eventos de pagamento (padrão Publish/Subscribe)
> 
> Esta arquitetura permite que cada serviço seja desenvolvido, testado e escalado de forma independente, garantindo alta disponibilidade e resiliência.

### Estrutura de Pastas

```
src/
├── main/                    # Camada de apresentação
│   ├── routes/             # Definição das rotas da API
│   ├── adapters/           # Adaptadores de requisição
│   ├── composers/          # Injeção de dependências
│   ├── server/            # Configuração do servidor
│   └── workers/           # 🆕 Workers para processamento assíncrono (RabbitMQ)
├── modules/               # Módulos de negócio
│   ├── authenticate_admin/ # Autenticação de administradores
│   ├── authenticate_user/  # Autenticação de usuários
│   ├── pet/               # Domínio de pets
│   ├── schedule/          # Domínio de agendamentos
│   ├── service_types/     # Domínio de tipos de serviços
│   └── user/              # Domínio de usuários (inclui pagamentos)
├── infra/                 # Camada de infraestrutura
│   ├── db/               # Configurações do banco
│   │   ├── entities/     # Entidades do banco
│   │   ├── repositories/ # Repositórios
│   │   └── settings/     # Configurações de conexão
│   └── docs/             # Documentação OpenAPI
├── drivers/              # Drivers externos
│   ├── jwt/             # Serviços JWT
│   ├── password_hasher/ # Hash de senhas
│   ├── email_sender/    # Serviço de envio de emails
│   └── payment_gateway/ # 🆕 Gateway de comunicação com microserviço de pagamentos
├── presentation/         # Camada de apresentação
│   ├── controllers/     # Controladores
│   ├── http_types/      # Tipos HTTP
│   └── interfaces/      # Interfaces de controladores
├── middlewares/          # Middlewares de autenticação
├── errors/              # Tratamento de erros
└── tests/               # Testes automatizados
```

## 📋 Pré-requisitos

- **Python 3.12+**
- **Docker** e **Docker Compose**
- **Git**
- **RabbitMQ** (para processamento de eventos de pagamento)

> **Nota**: O RabbitMQ é necessário apenas se você estiver trabalhando com o sistema completo de pagamentos. Para desenvolvimento local sem pagamentos, ele pode ser opcional.

## 🚀 Instalação

### 🐳 Opção 1: Instalação com Docker (Recomendada)

#### 1. Clone o repositório
```bash
git clone https://github.com/Andremelo001/schedule-pet-shop.git
cd schedule-pet-shop
```

#### 2. Configure as variáveis de ambiente
```bash
# Crie o arquivo .env baseado no exemplo
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

#### 3. Inicie toda a aplicação com Docker
```bash
# Inicia o banco de dados e a aplicação
docker-compose up -d --build
```

> **Nota**: Este comando irá:
> - Criar uma rede compartilhada com o microserviço de pagamentos
> - Iniciar o PostgreSQL na porta 5432
> - Iniciar a aplicação FastAPI na porta 8000
> - Configurar healthcheck para garantir que o banco esteja pronto

#### 4. Execute as migrations (primeira vez)
```bash
# Execute as migrations para criar as tabelas
docker-compose exec app uv run alembic upgrade head
```

#### 5. (Opcional) Inicie o Worker de Pagamentos
```bash
# Se estiver usando o sistema completo com RabbitMQ
docker-compose exec app python -m src.main.workers.payment_events_consumer
```

A API estará disponível em: `http://localhost:8000`
A documentação da API estará em: `http://localhost:8000/docs`

---

### 💻 Opção 2: Instalação Local (Desenvolvimento)

#### 1. Clone o repositório
```bash
git clone https://github.com/Andremelo001/schedule-pet-shop.git
cd schedule-pet-shop
```

#### 2. Configure o ambiente virtual
```bash
# Instale o UV (se ainda não tiver)
pip install uv

# Crie e ative o ambiente virtual
uv venv
# No Windows
.venv\Scripts\activate
# No Linux/Mac
source .venv/bin/activate

# Instale as dependências
uv pip sync pyproject.toml
```

#### 3. Configure as variáveis de ambiente
```bash
# Crie o arquivo .env baseado no exemplo
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

#### 4. Inicie apenas o banco de dados
```bash
# Inicia apenas o PostgreSQL
docker-compose up db -d
```

#### 5. Execute as migrations
```bash
# Execute as migrations para criar as tabelas
alembic upgrade head
```

#### 6. Inicie a aplicação localmente
```bash
fastapi dev src/main/server/server.py
```

#### 7. (Opcional) Inicie o Worker de Pagamentos
```bash
# Em outro terminal, se estiver usando o sistema completo com RabbitMQ
python -m src.main.workers.payment_events_consumer
```

A API estará disponível em: `http://localhost:8000`  
A documentação da API estará em: `http://localhost:8000/docs`

## 📋 API Endpoints

### 👥 Clientes (`/clients`)
- `POST /create` - Cadastrar novo cliente
- `GET /find` - Buscar cliente por CPF (Admin)
- `PUT /update` - Atualizar dados do cliente (Admin)
- `DELETE /delete` - Excluir cliente (Admin)
- `POST /login` - Login de cliente
- `GET /get_client_with_pets_and_schedules` - Relatório completo do cliente (Admin)
- `GET /pay_schedule` - Gerar pagamento Pix para agendamento (Cliente autenticado)
- `GET /finder_payment` - Consultar status de pagamento por agendamento (Público)

### 🐕 Pets (`/pets`)
- `POST /create` - Cadastrar novo pet (Cliente)
- `GET /get_all_pets` - Listar pets do cliente (Cliente)
- `GET /finder` - Buscar pet específico (Cliente)
- `PUT /update` - Atualizar dados do pet (Cliente)
- `DELETE /delete` - Excluir pet (Cliente)

### 📅 Agendamentos (`/schedules`)
- `POST /create` - Criar agendamento com validações completas (Cliente)
- `POST /request_cancel_schedule` - Solicitar cancelamento com envio de email (Cliente)
- `POST /cancel_schedule` - Cancelar agendamento via token JWT do email (Token JWT)
- `DELETE /delete` - Excluir agendamento (Admin)
- `GET /list` - Listar todos agendamentos (Admin)
- `GET /list_schedules_actives` - Listar agendamentos ativos/pagos (Admin)

### 🛠️ Serviços (`/services`)
- `POST /create` - Cadastrar serviço (Admin)
- `GET /list` - Listar todos serviços (Admin)
- `PUT /update` - Atualizar serviço (Admin)
- `DELETE /delete` - Excluir serviço (Admin)

### 👨‍💼 Admin (`/admin`)
- `POST /login` - Login de administrador

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de Dados PostgreSQL (usado pelo Docker)
POSTGRES_DB=db_petshop
POSTGRES_USER=petshop
POSTGRES_PASSWORD=sua_senha_segura
POSTGRES_PORT=5432

# URL de Conexão (usada pela aplicação)
DATABASE_URL="postgresql+asyncpg://petshop:sua_senha_segura@localhost:5432/db_petshop"
DATABASE_URL_DOCKER="postgresql+asyncpg://petshop:sua_senha_segura@db:5432/db_petshop"

# JWT
JWT_SECRET=your-super-secret-jwt-key-muito-segura
JWT_ALGORITHM=HS256
JWT_EXPIRATION_TIME=3600

# Admin
SENHA_ADMIN="sua_senha_admin_segura"

# Email (SMTP) - Configuração para envio de notificações
MAIL_HOST="smtp.ethereal.email"
MAIL_PORT="587"
MAIL_USERNAME="seu_email"
MAIL_PASSWORD="senha_email"

MICROSERVICE_URL="http://microservice_payments:8000"

# RabbitMQ - Mensageria para eventos de pagamento
RABBITMQ_URL="amqp://guest:guest@localhost:5672/"
```

> **🔒 Segurança**: 
> - Nunca commite o arquivo `.env` no repositório
> - Use senhas fortes e únicas
> - Em produção, use variáveis de ambiente do sistema

## 🏛️ Modelo de Dados

```mermaid
erDiagram
    Admin {
        uuid id PK
        string name
        string senha
        string user UK
    }

    Client {
        uuid id PK
        string name
        string cpf UK
        string senha
        string email
        int age
    }

    Pet {
        uuid id PK
        string name
        string breed
        int age
        int size_in_centimeters
        uuid client_id FK
    }

    Schedule {
        uuid id PK
        date date_schedule
        time time_schedule
        uuid client_id FK
        uuid pet_id FK
        float total_price_schedule
        bool schedule_active
    }

    Services {
        uuid id PK
        int duration_in_minutes
        string type_service
        float price
    }

    ScheduleServices {
        uuid services_id FK
        uuid schedule_id FK
    }

    Client ||--o{ Pet : "possui"
    Client ||--o{ Schedule : "agenda"
    Pet ||--o{ Schedule : "participa de"
    Schedule ||--o{ ScheduleServices : "contém"
    Services ||--o{ ScheduleServices : "usado em"
``` 

### 📝 Descrição das Entidades

- **Admin**: Usuários administradores do sistema
- **Client**: Clientes/proprietários de pets
- **Pet**: Animais de estimação cadastrados
- **Schedule**: Agendamentos de serviços (vinculados a cliente e pet)
- **Services**: Tipos de serviços oferecidos pelo petshop
- **ScheduleServices**: Tabela de relacionamento N:N entre agendamentos e serviços

### 🔑 Regras de Negócio do Modelo

1. Um cliente pode ter múltiplos pets
2. Um agendamento está vinculado a um único cliente e um único pet
3. Um agendamento pode ter múltiplos serviços (máximo 3)
4. A exclusão de um cliente remove em cascata seus pets e agendamentos
5. A exclusão de um pet remove em cascata seus agendamentos
6. O campo `schedule_active` indica se o agendamento foi pago

## 🔄 Workers e Processamento Assíncrono

### Worker de Eventos de Pagamento

A aplicação possui um worker dedicado que consome eventos de pagamento do RabbitMQ:

**Localização**: `src/main/workers/payment_events_consumer.py`

#### Como Iniciar o Worker:

```bash
# Certifique-se de que o RabbitMQ está rodando
# Configure a variável RABBITMQ_URL no arquivo .env

# Execute o worker
python -m src.main.workers.payment_events_consumer
```

#### Fluxo de Processamento:

1. Cliente solicita pagamento via endpoint `/clients/pay_schedule`
2. Sistema gera pagamento no microserviço de pagamentos
3. Microserviço publica evento no RabbitMQ quando pagamento é confirmado
4. Worker consome evento e atualiza status do agendamento
5. Agendamento é marcado como ativo (`schedule_active = True`)

#### Estrutura de Eventos:

```json
{
  "schedule_id": "uuid-do-agendamento",
  "status": "paid",
  "payment_date": "2024-12-02T10:30:00"
}
```

## 🧪 Testes

A aplicação possui cobertura de testes automatizados para garantir a qualidade do código.

### Estrutura de Testes

```
src/tests/
├── modules/                    # Testes de casos de uso
│   ├── authenticate_admin/    # Testes de autenticação admin
│   ├── authenticate_user/     # Testes de autenticação usuário
│   ├── pet/                   # Testes de gestão de pets
│   ├── schedule/              # Testes de agendamentos
│   ├── service_types/         # Testes de serviços
│   └── user/                  # Testes de gestão de clientes
└── infra/                     # Testes de repositórios
    └── db/
        └── repositories/      # Testes de acesso a dados
```

### Executar Testes

```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=src --cov-report=html

# Executar testes de um módulo específico
pytest src/tests/modules/schedule/

# Executar testes com output detalhado
pytest -v

# Executar testes em paralelo (mais rápido)
pytest -n auto
```

### Categorias de Testes

#### ✅ Testes de Use Cases
- Testes unitários de lógica de negócio
- Validação de regras de negócio
- Testes com mocks de repositórios

#### ✅ Testes de Repositórios
- Testes de integração com banco de dados
- Validação de queries e operações CRUD
- Testes de relacionamentos entre entidades

#### ✅ Tecnologias de Teste
- **Pytest**: Framework principal
- **Pytest-asyncio**: Suporte para testes assíncronos
- **Pytest-mock**: Criação de mocks
- **Fixtures**: Reutilização de configurações de teste

## 🚀 Recursos Adicionais

### 📖 Documentação da API

A API possui documentação interativa automática gerada pelo FastAPI:

- **Swagger UI**: `http://localhost:8000/docs` - Interface interativa para testar endpoints
- **ReDoc**: `http://localhost:8000/redoc` - Documentação alternativa mais limpa
- **OpenAPI JSON**: `http://localhost:8000/openapi.json` - Especificação OpenAPI completa

### 🔒 Segurança Implementada

- **JWT Tokens**: Autenticação stateless com tokens JWT
- **Tokens por Perfil**: Tokens diferentes para Admin e Cliente
- **Token de Cancelamento**: Token específico com tempo limitado para cancelamento
- **Hash de Senhas**: Bcrypt para armazenamento seguro de senhas
- **Middleware de Autenticação**: Validação automática de permissões
- **Proteção de Rotas**: Endpoints protegidos por perfil de usuário

### 📊 Padrões e Princípios

Este projeto segue diversos padrões e princípios de engenharia de software:

- **Clean Architecture**: Separação clara de camadas
- **SOLID**: Princípios de design orientado a objetos
- **Repository Pattern**: Abstração de acesso a dados
- **Dependency Injection**: Via composers/factories
- **Use Cases**: Lógica de negócio isolada
- **DTOs**: Validação de dados de entrada
- **Error Handling**: Tratamento centralizado de erros
- **Async/Await**: Programação assíncrona para melhor performance

### 🎨 Boas Práticas

- ✅ Código tipado (Type Hints)
- ✅ Validação de dados com Pydantic
- ✅ Testes automatizados
- ✅ Migrations versionadas
- ✅ Logs estruturados
- ✅ Tratamento de erros consistente
- ✅ Documentação de API automática
- ✅ Containerização com Docker
- ✅ Variáveis de ambiente para configuração
- ✅ Cascade deletion para integridade referencial

## 👨‍💻 Autor

**André Melo**
- GitHub: [@Andremelo001](https://github.com/Andremelo001)
- LinkedIn: [André Melo](https://www.linkedin.com/in/melooandree/)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório! 
