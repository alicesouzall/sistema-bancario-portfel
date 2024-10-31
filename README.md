# Documentação

### Env
- copie o arquivo `.env.example` e cole dentro seu arquivo `.env` com as credenciais do seu banco de dados **PostgreSQL**
- as variáveis de ambiente necessárias são:
    - `DATABASE_HOST` ("portfel_db")
    - `DATABASE_NAME`
    - `DATABASE_USERNAME`
    - `DATABASE_PASSWORD`
    - `DATABASE_PORT`

### Rodar Aplicação com Docker
- rode no terminal `docker compose up --build`

### Testes
- rode no terminal `poetry run pytest` para rodar todos os testes

## Swagger
- entre em `{API_URL}/docs` ou `{API_URL}/redoc` para acessar a documentação de rotas oferecida pelo Swagger UI
- entre em `{API_URL}/openapi.json` para acessar o json do Swagger

# Sobre
    Este app representa um sistema bancário simples, que permite a criação de contas com um saldo inicial de R$ 0.00, realização de depósitos e realização de saques.
- Este sistema foi desenvolvido com a linguagem **Python**, juntamente com a biblioteca **FastAPI** para criação de API e o **Poetry**, responsável por gerenciar os pacotes, ambientes virtuais e dependências do python.
- Este sistema foi desenvolvido com a arquitetura **Ports And Adapters** ou **Arquitetura Hexagonal**, uma arquitetura baseada em **DDD**, devido a sua fácil adaptação com quaisquer mudanças futuras, além de permitir uma grande escalabilidade, testagem e segurança (requisitos importantíssimos em um sistema bancário real).
- No banco temos duas tabelas:
    - **acount**: salva o número da conta (number) e o saldo atual (balance).
    - **logs**: salva todas as transações entre contas e os logs de erro de qualquer operação.
- Este sistema verifica erros de:
    - saldo insuficiente
    - valor de transação inválido
    - conta (remetente e de destino) inexistente
    - conta remetente e conta de destino são iguais
    - senha do banco incorreta
    - connection timeout
    - erros internos a nível de desenvolvimento
    - ...entre outros
- Os testes abrangem os cenários de transações de depósito, transferência e saque, e foram desenvolvidos com a biblioteca **Pytest**.

