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

## API: endpoints e exemplos

- **Base**: `http://127.0.0.1:8000/api/`
- **Eventos**: `/api/events/` — CRUD completo
- **Guilds**: `/api/guilds/` — CRUD completo
- **Players**: `/api/players/` — CRUD completo
- **Users**: `/api/users/` — CRUD completo

### Exemplos de Requisições (usando `curl`)

**Listar eventos**:

```bash
curl -sS http://127.0.0.1:8000/api/events/
```

**Criar um evento**:

```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "type": "player_level_up",
    "details": {"level": 42, "rewards": ["sword","gold"]},
    "player": null,
    "guild": null
  }'
```

**Recuperar um evento**:

```bash
curl http://127.0.0.1:8000/api/events/<event_uuid>/
```

**Atualizar um evento (PATCH)**:

```bash
curl -X PATCH http://127.0.0.1:8000/api/events/<event_uuid>/ \
  -H "Content-Type: application/json" \
  -d '{"details": {"level": 43}}'
```

**Deletar um evento**:

```bash
curl -X DELETE http://127.0.0.1:8000/api/events/<event_uuid>/
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

**Autenticação**: Não implementada nos endpoints. Pode ser adicionada via DRF `permissions.IsAuthenticated`.

**Estrutura arquitetural**: Todos os apps seguem o mesmo padrão:

**Type checking**: Configurado via `pyproject.toml` com `django-stubs` para suporte a type hints.
**Estrutura arquitetural**: Todos os apps seguem o mesmo padrão:

- `models.py`: Modelos com UUID como chave primária
- `serializers.py`: ModelSerializer com campos read-only (id, created_at)
- `views.py`: ModelViewSet para CRUD automático
- `urls.py`: Router registration para endpoints RESTful
- `tests.py`: Testes de modelo e API (APITestCase)

**Type checking**: Configurado via `pyproject.toml` com `django-stubs` para suporte a type hints.

**INSTALLED_APPS**: Utiliza `"rest_framework"` como identificador correto do Django REST Framework.

## Melhorias sugeridas

- Implementar autenticação/permissões nas APIs
- Adicionar validações específicas aos serializers
- Adicionar paginação nos endpoints list
- Implementar filtros e busca nos endpoints

## Fluxo rápido de verificação local

1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py createsuperuser`
4. `python manage.py runserver`
5. Acesse `http://127.0.0.1:8000/api/`

---

**Arquivo principal**: `manage.py` — use-o para comandos de migração, testes e execução.
