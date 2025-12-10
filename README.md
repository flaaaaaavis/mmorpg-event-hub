# mmorpg-event-hub

## Resumo

- **Projeto**: Serviço simples em Django + Django REST Framework para registrar "events" (eventos) relacionados a `Player`, `Guild` e `User`.

## Requisitos

- **Python**: 3.8+ (recomendado 3.10+)
- **Banco de dados**: SQLite (padrão, arquivo `db.sqlite3`)
- **Dependências principais**: `Django`, `djangorestframework`

## Instalação & Execução

**Criar ambiente virtual**:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (bash.exe)
```

**Instalar dependências**:

```bash
pip install -r requirements.txt
```

**Aplicar migrações e criar superusuário**:

```bash
python manage.py migrate
python manage.py createsuperuser
```

**Rodar o servidor de desenvolvimento**:

```bash
python manage.py runserver
```

O servidor ficará disponível em `http://127.0.0.1:8000/`.

## Como rodar os testes

Executar todos os testes do projeto:

```bash
python manage.py test apps --verbosity=2
```

Todos os apps contêm testes em `tests.py`. O projeto inclui 42 testes cobrindo modelos e endpoints de API.

## API: endpoints e autenticação

### Base URL e autenticação

- **Base**: `http://127.0.0.1:8000/api/`
- **Autenticação**: Token (DRF) ou Session (para UI)
- **Permissões**: `IsAuthenticatedOrReadOnly` — leitura pública, escrita autenticada

### Obter Token de Autenticação

```bash
curl -X POST http://127.0.0.1:8000/api/token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'
```

Resposta:
```json
{"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}
```

### Usar Token em Requisições

Adicione o header:
```bash
-H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Endpoints Disponíveis

| Recurso | Método | Endpoint | Autenticação |
|---------|--------|----------|--------------|
| Events | GET | `/api/events/` | Não requerida |
| Events | POST | `/api/events/` | **Requerida** |
| Events | GET | `/api/events/{id}/` | Não requerida |
| Events | PUT/PATCH | `/api/events/{id}/` | **Requerida** |
| Events | DELETE | `/api/events/{id}/` | **Requerida** |
| Guilds | GET | `/api/guilds/` | Não requerida |
| Guilds | POST | `/api/guilds/` | **Requerida** |
| Guilds | GET | `/api/guilds/{id}/` | Não requerida |
| Guilds | PUT/PATCH | `/api/guilds/{id}/` | **Requerida** |
| Guilds | DELETE | `/api/guilds/{id}/` | **Requerida** |
| Players | GET | `/api/players/` | Não requerida |
| Players | POST | `/api/players/` | **Requerida** |
| Players | GET | `/api/players/{id}/` | Não requerida |
| Players | PUT/PATCH | `/api/players/{id}/` | **Requerida** |
| Players | DELETE | `/api/players/{id}/` | **Requerida** |
| Users | GET | `/api/users/` | Não requerida |
| Users | POST | `/api/users/` | **Requerida** |
| Users | GET | `/api/users/{id}/` | Não requerida |
| Users | PUT/PATCH | `/api/users/{id}/` | **Requerida** |
| Users | DELETE | `/api/users/{id}/` | **Requerida** |

### Exemplos de Requisições

#### Events

**Listar eventos (sem autenticação)**:

```bash
curl -sS http://127.0.0.1:8000/api/events/
```

**Criar um evento (com token)**:

```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "type": "player_level_up",
    "details": {"level": 42, "rewards": ["sword", "gold"]},
    "player": null,
    "guild": null
  }'
```

**Atualizar evento (PATCH com token)**:

```bash
curl -X PATCH http://127.0.0.1:8000/api/events/<uuid>/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"details": {"level": 43}}'
```

**Deletar evento (com token)**:

```bash
curl -X DELETE http://127.0.0.1:8000/api/events/<uuid>/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Guilds

**Listar guildas**:

```bash
curl -sS http://127.0.0.1:8000/api/guilds/
```

**Criar guilda (com token)**:

```bash
curl -X POST http://127.0.0.1:8000/api/guilds/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "name": "Minha Guilda",
    "score": "1000",
    "awards": ["first_win"]
  }'
```

#### Players

**Listar players**:

```bash
curl -sS http://127.0.0.1:8000/api/players/
```

**Criar player (com token)**:

```bash
curl -X POST http://127.0.0.1:8000/api/players/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "user": "<user_uuid>",
    "guild": "<guild_uuid>",
    "awards": ["achievement1"]
  }'
```

#### Users

**Listar users**:

```bash
curl -sS http://127.0.0.1:8000/api/users/
```

**Criar user (com token)**:

```bash
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"username": "novo_usuario"}'
```

## Modelos

### Event

- `id`: UUID (chave primária)
- `type`: string (até 100 caracteres)
- `details`: JSONField (payload livre)
- `player`: FK para `Player` (nullable)
- `guild`: FK para `Guild` (nullable)
- `created_at`: timestamp (auto)

### Guild

- `id`: UUID (chave primária)
- `name`: string (até 100 caracteres)
- `score`: string (até 100 caracteres)
- `awards`: JSONField (lista)
- `created_at`: timestamp (auto)

### Player

- `id`: UUID (chave primária)
- `user`: FK para `User` (obrigatório)
- `guild`: FK para `Guild` (nullable)
- `awards`: JSONField (lista)
- `created_at`: timestamp (auto)

### User

- `id`: UUID (chave primária)
- `username`: string única (até 150 caracteres)
- `created_at`: timestamp (auto)

## Decisões técnicas

**Banco de desenvolvimento**: SQLite por padrão (`db.sqlite3`). Em produção, recomenda-se PostgreSQL.

**Autenticação**: Implementada via DRF Token (`rest_framework.authtoken`). Endpoints GET são públicos (leitura). Endpoints POST/PUT/PATCH/DELETE requerem token de autenticação. Obtenha o token enviando credenciais para `/api/token-auth/`.

**Estrutura arquitetural**: Todos os apps seguem o mesmo padrão:

- `models.py`: Modelos com UUID como chave primária
- `serializers.py`: ModelSerializer com campos read-only (id, created_at)
- `views.py`: ModelViewSet para CRUD automático
- `urls.py`: Router registration para endpoints RESTful
- `tests.py`: Testes de modelo e API (APITestCase)

**Type checking**: Configurado via `pyproject.toml` com `django-stubs` para suporte a type hints.

**INSTALLED_APPS**: Utiliza `"rest_framework"` como identificador correto do Django REST Framework.

## Melhorias sugeridas

- Adicionar validações específicas aos serializers (ex: validação de `type` de evento)
- Adicionar paginação nos endpoints list (DRF pagination)
- Implementar filtros e busca nos endpoints (django-filter)
- Adicionar rate limiting para proteção contra abuso
- Expandir testes com casos de validação e edge cases

## Fluxo rápido de verificação local

1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py createsuperuser`
4. `python manage.py runserver`
5. Acesse `http://127.0.0.1:8000/api/`

---

**Arquivo principal**: `manage.py` — use-o para comandos de migração, testes e execução.
