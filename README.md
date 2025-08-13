# API para gerenciamento de PetShop
API para gerenciamento de PetShop - Controle de clientes, pets, agendamentos e serviços veterinários.

# Tecnologias Utilizadas
    - Python
    - FastApi
    - PostgreSQL
    - SQLModel
    - Docker
    - Pytest

# Diagrama da Aplicação
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
