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
  
## Uso
Suba a aplicação com o comando:

```bash
 python -m uvicorn client_service.app.api.core.config:app --reload
```

## Testes
Cobertura de 100% dos endpoints.

  