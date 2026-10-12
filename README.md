# Restaurante Manager

Aplicação web para cadastro e gestão de restaurantes, construída com **FastAPI**, **Jinja2** e **SQLite**. Tem páginas HTML renderizadas no servidor e uma API REST para as mesmas operações.

Projeto de estudo focado em boas práticas de backend com Python: arquitetura em camadas, injeção de dependências, validação com Pydantic e armazenamento seguro de senhas.

## Funcionalidades

- **Contas de usuário**: cadastro, login e logout. A sessão fica num cookie `httponly`.
- **Senhas seguras**: guardadas apenas como hash `scrypt` com salt aleatório e comparadas em tempo constante (`hmac.compare_digest`).
- **CRUD de restaurantes**: cadastrar, listar, ver detalhes, editar e excluir.
- **Ativar e desativar** restaurantes sem apagar o cadastro.
- **Painel inicial** com o total de restaurantes, quantos estão ativos e quantos estão desativados.
- **API REST** com documentação interativa automática (Swagger) em `/docs`.
- **Interface responsiva** que funciona sem JavaScript. O JS só melhora a experiência: menu mobile, mostrar senha e confirmação de exclusão.

## Tecnologias

| Camada | Tecnologia |
| --- | --- |
| Framework web | [FastAPI](https://fastapi.tiangolo.com/) |
| Servidor ASGI | [Uvicorn](https://www.uvicorn.org/) |
| Validação | [Pydantic v2](https://docs.pydantic.dev/) |
| Templates | [Jinja2](https://jinja.palletsprojects.com/) |
| Banco de dados | SQLite (`sqlite3` da biblioteca padrão) |
| Front-end | HTML, CSS e JavaScript puro |

## Arquitetura

O código é dividido em camadas, e cada uma tem uma única responsabilidade:

```
Requisição → routers → repositories → database (SQLite)
                │
                ├── schemas      (validação de entrada/saída)
                ├── services     (regras como hash de senha)
                └── templates    (renderização HTML)
```

```
app/
├── main.py              # Cria a aplicação, registra rotas, arquivos estáticos e tratamento de erros
├── dependencies.py      # Injeção de dependências (banco e repositórios)
├── database/
│   └── database.py      # Conexão SQLite e criação das tabelas
├── repositories/        # Acesso a dados (consultas SQL parametrizadas)
│   ├── restaurante_repository.py
│   └── usuario_repository.py
├── schemas/             # Modelos Pydantic de entrada e saída
├── services/
│   └── auth_service.py  # Geração e verificação de hash de senha
├── routers/
│   ├── restaurantes.py           # Operações de restaurantes (API e formulários)
│   ├── usuarios.py               # Registro, login, logout e /me
│   ├── frontend.py               # Página inicial
│   ├── frontend_restaurantes.py  # Páginas de restaurantes
│   └── frontend_usuarios.py      # Páginas de login e registro
├── templates/           # Páginas Jinja2 (base.html define o layout)
└── static/              # CSS e JavaScript
```

**Decisões de design:**

- **Repository Pattern**: as rotas não escrevem SQL; elas chamam métodos do repositório. Isso facilita trocar o banco ou criar testes com um repositório falso.
- **Injeção de dependências** com `Depends`: o banco e os repositórios são entregues às rotas pelo FastAPI, sem variáveis globais espalhadas pelo código.
- **Rotas da API reaproveitadas nas páginas**: as páginas HTML usam as funções da API como dependência (por exemplo, `Depends(listar_restaurantes)`), assim a mesma lógica serve a API e o site.
- **Post/Redirect/Get**: depois de um formulário, a aplicação redireciona com `303 See Other`, o que evita reenviar os dados ao atualizar a página.
- **SQL parametrizado** (`?`) em todas as consultas, para prevenir SQL injection.

## Como executar

**Pré-requisito:** Python 3.10 ou superior.

```bash
# 1. Clone o repositório
git clone https://github.com/HigorBackend-Devloper/API-RESTAURANTE-FASTAPI.git
cd API-RESTAURANTE-FASTAPI

# 2. Crie e ative um ambiente virtual
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
uvicorn app.main:app --reload
```

Depois acesse:

- **Aplicação:** http://127.0.0.1:8000
- **Documentação da API (Swagger):** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

O banco `restaurante.db` e suas tabelas são criados automaticamente na primeira execução.

## Rotas

### Páginas e formulários

Formulários HTML só enviam `GET` e `POST`, por isso as ações do site usam `POST` com um caminho descritivo.

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/` | Painel com totais e lista de restaurantes |
| GET | `/registro` | Página de cadastro de usuário |
| POST | `/registro` | Cria a conta (`nome`, `email`, `senha`, `confirmar_senha`) |
| GET | `/login` | Página de login |
| POST | `/login` | Autentica e cria o cookie de sessão |
| GET / POST | `/logout` | Encerra a sessão |
| GET | `/restaurantes` | Lista de restaurantes |
| GET | `/restaurantes/novo` | Formulário de cadastro |
| POST | `/restaurantes` | Cadastra um restaurante (`nome`, `categoria`, `ativo`) |
| GET | `/restaurantes/{id}` | Detalhes do restaurante |
| GET | `/restaurantes/{id}/editar` | Formulário de edição |
| POST | `/restaurantes/{id}/editar` | Salva a edição |
| POST | `/restaurantes/{id}/status` | Ativa ou desativa (`ativo=true/false`) |
| POST | `/restaurantes/{id}/excluir` | Exclui o restaurante |

### API (JSON)

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/restaurante/{id}` | Busca um restaurante pelo id |
| PUT | `/restaurante?restaurante_id={id}` | Substitui todos os campos |
| PATCH | `/restaurante/{id}` | Atualiza só os campos enviados |
| GET | `/me` | Dados do usuário logado |
| GET | `/health` | Verifica se a API está no ar |

Exemplo de atualização parcial:

```bash
curl -X PATCH http://127.0.0.1:8000/restaurante/1 \
  -H "Content-Type: application/json" \
  -d '{"ativo": false}'
```

## Modelo de dados

```sql
usuarios     (id, nome, email UNIQUE, senha [hash], criado_em)
restaurantes (id, nome, categoria, ativo [0/1], criado_em)
```

## Próximos passos

- [ ] Testes automatizados com `pytest` e `TestClient`
- [ ] Sessão com token assinado (JWT) em vez do id do usuário no cookie
- [ ] Proteger as rotas de restaurantes para usuários autenticados
- [ ] Busca e filtro por situação na listagem
- [ ] Proteção CSRF nos formulários
- [ ] `Dockerfile` para execução em contêiner

## Autor

**Higor** · [GitHub @HigorBackend-Devloper](https://github.com/HigorBackend-Devloper)
