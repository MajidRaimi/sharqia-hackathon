# Sharqia Hackathon

Monorepo powered by [Turborepo](https://turbo.build/) + [Bun](https://bun.sh/) with a Next.js frontend and FastAPI backend.

## Prerequisites

- [Bun](https://bun.sh/) >= 1.2
- [uv](https://docs.astral.sh/uv/) >= 0.8
- [Docker](https://www.docker.com/) (for PostgreSQL)
- Python >= 3.12

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/MajidRaimi/sharqia-hackathon.git
cd sharqia-hackathon
```

### 2. Install dependencies

```bash
bun install
```

This installs all Node.js dependencies across the monorepo, including Turborepo and mprocs.

### 3. Set up the API environment

```bash
cp apps/api/.env.example apps/api/.env
```

Edit `apps/api/.env` with your values:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sharqia
SECRET_KEY=<generate-a-secure-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
DEBUG=true
```

### 4. Install Python dependencies

```bash
cd apps/api
uv sync
cd ../..
```

### 5. Run the project

```bash
bun run dev
```

This launches [mprocs](https://github.com/pvolok/mprocs) which starts:

- **db** -- PostgreSQL 17 (Docker container) on port `5432`
- **api** -- FastAPI dev server on port `8000`

Use the arrow keys in the mprocs TUI to switch between process logs. Press `q` to quit.

### 6. Verify

- API docs: http://localhost:8000/api/docs
- API redoc: http://localhost:8000/api/redoc

## Project Structure

```
sharqia-hackathon/
├── apps/
│   ├── web/          Next.js 15 frontend (port 3000)
│   └── api/          FastAPI backend (port 8000)
├── packages/
│   ├── ui/           Shared React component library
│   ├── typescript-config/
│   └── eslint-config/
├── mprocs.yaml       Process runner config
├── turbo.json        Turborepo pipeline
└── package.json      Root workspace config
```

## Scripts

| Command | Description |
|---------|-------------|
| `bun run dev` | Start all services via mprocs |
| `bun run build` | Build all apps and packages |
| `bun run lint` | Lint the entire monorepo |
| `bun run check-types` | Type-check all packages |

## Tech Stack

**Frontend** -- Next.js 15, React 19, TypeScript

**Backend** -- FastAPI, SQLAlchemy (async), PostgreSQL, Alembic, Pydantic v2

**Tooling** -- Turborepo, Bun, uv, ruff, mprocs
