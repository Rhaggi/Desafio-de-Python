# Projeto Banco Javer

Aplicação de Api de contas bancárias de clientes com banco de dados

## Índice

- [Sobre](#sobre)
- [Tecnologias](#tecnologias)
- [Uso](#uso)
- [Testes](#testes)

## Sobre

Este é um projeto desenvolvido com Python para o gerenciamento simples de contas bancarias. A aplicação cliente se comunica com a aplicacao do banco de dados e possui documentacao completa de ambos os serviços pela FastApi.

## Tecnologias

O projeto utiliza as seguintes tecnologias:

- [Sqlite3]
- [FastApi]
- [Pathlib]
- [sqlalchemy]
- [requests]
- [httpx]

  
## Uso
Suba as duas aplicações em terminais diferentes com o comando:

```bash
 python -m uvicorn client_service.app.api.core.config:app --reload --port 8000
```

```bash
 python -m uvicorn database_service.app.api.v1.core.config_db:app_db --reload --port 8001
```

## Testes
Cobertura de 100% dos endpoints.

  