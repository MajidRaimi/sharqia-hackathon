# API - FastAPI Application

## Overview

This is a production-ready FastAPI application serving as the backend API for the Sharqia Hackathon project. It is designed to handle high-throughput workloads including REST APIs, AI/ML service integrations, and real-time data processing.

## Tech Stack

- **Framework**: FastAPI (async, high-performance Python web framework)
- **Database**: PostgreSQL (via SQLAlchemy async + asyncpg driver)
- **Migrations**: Alembic (async migration support)
- **Auth**: JWT-based authentication (python-jose + passlib/bcrypt)
- **Validation**: Pydantic v2 with pydantic-settings for config management
- **Dependency Manager**: uv (with uv.lock for reproducible installs)
- **Formatter/Linter**: ruff (single quotes enforced, production-grade config)
- **Runtime**: uvicorn (ASGI server)

## Project Structure

Follows the `@.agents/skills/fastapi-templates/` skill pattern strictly:

```
apps/api/
├── app/
│   ├── main.py                 # Application entry point, lifespan, middleware
│   ├── api/
│   │   ├── dependencies.py     # Shared DI (auth, db session)
│   │   └── v1/
│   │       ├── router.py       # v1 API router aggregation
│   │       └── endpoints/      # Route handlers (thin, delegate to services)
│   │           ├── health.py
│   │           └── users.py
│   ├── core/
│   │   ├── config.py           # Settings via pydantic-settings + .env
│   │   ├── database.py         # Async engine, session factory, get_db
│   │   └── security.py         # JWT creation/verification, password hashing
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── base.py
│   │   └── user.py
│   ├── schemas/                # Pydantic request/response schemas
│   │   └── user.py
│   ├── services/               # Business logic layer
│   │   └── user_service.py
│   └── repositories/           # Data access layer (DB queries)
│       ├── base.py
│       └── user_repository.py
├── alembic/                    # Database migrations
│   ├── env.py
│   └── versions/
├── alembic.ini
├── tests/
│   └── conftest.py
├── pyproject.toml              # Project metadata + dependencies
├── ruff.toml                   # Ruff formatter/linter config
├── .env.example                # Environment variable template
└── CLAUDE.md                   # This file
```

## Architecture Principles

1. **Layered Architecture**: Routes -> Services -> Repositories -> Database
2. **Async All The Way**: Every I/O operation is async (database, external APIs, AI calls)
3. **Dependency Injection**: FastAPI's `Depends()` for DB sessions, auth, config
4. **Repository Pattern**: All database access goes through repository classes
5. **Service Layer**: Business logic lives in services, never in route handlers
6. **Strong Typing**: Pydantic schemas for all request/response boundaries

## Key Conventions

### NO COMMENTS IN CODE

Do NOT write any comments in the codebase. No inline comments, no block comments, no docstrings. The code must be self-documenting through clear naming, type hints, and structure. This is a strict rule with zero exceptions.

### Dependency Management

- Use `uv` exclusively (never pip, never poetry)
- Always run `uv sync` after adding dependencies
- The `uv.lock` file MUST be committed - it ensures reproducible builds
- Add dependencies via `uv add <package>`
- Add dev dependencies via `uv add --dev <package>`

### Code Formatting

- Use `ruff` for all formatting and linting
- Run `ruff format .` and `ruff check --fix .` after every change
- Single quotes are enforced (`'` not `"`)
- Configured in `ruff.toml` at the api root

### Database

- PostgreSQL is the only supported database
- Use async SQLAlchemy with `asyncpg` driver
- Connection string format: `postgresql+asyncpg://user:pass@host:port/dbname`
- All migrations via Alembic (`alembic revision --autogenerate`, `alembic upgrade head`)

### API Versioning

- All endpoints are prefixed with `/api/v1/`
- New versions get a new directory under `app/api/v2/`, etc.
- Never break existing API contracts in a released version

### AI Services

This API is built to integrate with AI/ML services. When adding AI endpoints:
- Place AI-related endpoints in `app/api/v1/endpoints/`
- Create dedicated services in `app/services/` for AI logic
- Use async HTTP clients (httpx) for external AI API calls
- Stream responses where possible using FastAPI's `StreamingResponse`

## Skill Reference

All structural decisions, patterns, and templates for this application follow:
**`@.agents/skills/fastapi-templates/`**

Always consult that skill when creating new endpoints, services, repositories, or models.

## Running

```bash
cd apps/api
uv sync                          # Install dependencies
uv run alembic upgrade head      # Run migrations
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

Copy `.env.example` to `.env` and fill in values:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sharqia
SECRET_KEY=<generate-a-secure-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
DEBUG=true
```
