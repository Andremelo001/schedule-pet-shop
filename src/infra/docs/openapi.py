from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Schedule Pet Shop API",
        version="1.0.0",
        description="""
        ## API para Sistema de Agendamento de Pet Shop

        Esta API permite gerenciar um sistema completo de agendamento para pet shop, incluindo:

        ### Funcionalidades principais:
        * **Gestão de Clientes** - Cadastro, consulta, atualização e remoção de clientes
        * **Gestão de Pets** - Registro e gerenciamento dos animais de estimação
        * **Agendamento de Serviços** - Sistema de marcação de horários para serviços
        * **Gestão de Serviços** - Cadastro e gerenciamento dos tipos de serviços oferecidos
        * **Autenticação** - Sistema de login para clientes e administradores

        ### Autenticação:
        A API utiliza autenticação JWT (JSON Web Token). Para acessar endpoints protegidos:
        1. Faça login através do endpoint `/clients/login` ou `/admin/login`
        2. Use o token retornado no header `Authorization: Bearer <token>`

        ### Tipos de usuário:
        * **Cliente** - Pode gerenciar seus próprios pets e agendamentos
        * **Administrador** - Acesso completo ao sistema

        ---
        **Desenvolvido com FastAPI** 🚀
        """,
        routes=app.routes,
    )

    # garante que components exista
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    # adiciona o BearerAuth com mais detalhes
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Insira o token JWT obtido através do login. Formato: Bearer <token>"
    }

    # adiciona tags para organizar melhor a documentação
    openapi_schema["tags"] = [
        {
            "name": "Clients",
            "description": "Operações relacionadas aos clientes do pet shop"
        },
        {
            "name": "Pets", 
            "description": "Gerenciamento dos animais de estimação"
        },
        {
            "name": "Admin",
            "description": "Funcionalidades administrativas e autenticação de administradores"
        },
        {
            "name": "Schedules",
            "description": "Sistema de agendamento de serviços"
        },
        {
            "name": "Services",
            "description": "Gestão dos tipos de serviços oferecidos"
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema
