# URLPulse — Production-Grade URL Shortener

> **MLH Production Engineering Hackathon 2026**

A production-grade URL shortener built to survive chaos. Shorten URLs, track events, and prove your system can handle load, recover from failures, and alert when things break.

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Language** | Python 3.13 | Template default, team familiarity |
| **Framework** | Flask | Lightweight, hackathon-friendly |
| **ORM** | Peewee | Simple, DatabaseProxy pattern for connection pooling |
| **Database** | PostgreSQL 16 | Production-grade relational DB |
| **Cache** | Redis 7 | In-memory caching with TTL & LRU eviction |
| **WSGI Server** | Gunicorn | Multi-worker concurrent request handling |
| **Load Balancer** | Nginx | Round-robin across 3 app instances |
| **Containerization** | Docker + Docker Compose | Full stack orchestration |
| **Metrics** | Prometheus | Scrapes /metrics, stores time-series data |
| **Dashboards** | Grafana | Four Golden Signals visualization |
| **Alerting** | Alertmanager → Discord | Automated incident notifications |
| **CI/CD** | GitHub Actions | Test → Build → Deploy pipeline |
| **Infrastructure** | GCP + Terraform | Reproducible cloud deployment |
| **Load Testing** | k6 | Scriptable load tests (50/200/500 users) |
| **Package Manager** | uv | Fast Python dependency management |

## Architecture

```
Internet
   │
   ▼
┌─────────┐
│  Nginx  │  :80  (round-robin load balancer)
└────┬────┘
     │
     ├──────────────┬──────────────┐
     ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│  App 1  │  │  App 2  │  │  App 3  │  Flask + Gunicorn
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     ▼            ▼            ▼
┌─────────┐  ┌─────────┐
│ Postgres │  │  Redis  │
│   :5432  │  │  :6379  │
└──────────┘  └─────────┘

Observability:
  Prometheus (:9090) → Grafana (:3000) → Alertmanager (:9093) → Discord
```

## Data Model

- **User** — username, email, created_at
- **Url** — linked to a User, short_code (unique), original_url, title, is_active, timestamps
- **Event** — linked to both Url and User, event_type (created/updated/deleted), details (JSON)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Liveness check |
| `POST` | `/users` | Create a user |
| `GET` | `/users` | List all users |
| `GET` | `/users/<id>` | Get user by ID |
| `POST` | `/shorten` | Create a shortened URL |
| `POST` | `/update` | Update a URL |
| `POST` | `/delete` | Delete a URL |

## Running Locally (No Docker)

```bash
# 1. Install dependencies
uv sync

# 2. Configure environment — pick ONE option in .env
cp .env.example .env

# Option A: Supabase (recommended for teams — shared DB, no local setup)
#   Fill in your Supabase credentials in .env
#   Get them from: Supabase Dashboard → Connect → Connection string

# Option B: Local PostgreSQL
#   Uncomment the local block in .env and comment out the Supabase block
#   Make sure PostgreSQL is running locally:
#   brew install postgresql@16 && brew services start postgresql@16
#   createdb hackathon_db

# 3. Run the server
uv run run.py
# Server starts at http://localhost:5000

# 4. Verify it's working
curl http://localhost:5000/health
# → {"status":"ok"}
```

### Running Tests

```bash
uv run pytest --cov=app --cov-fail-under=70
```

## Project Structure

```
urlpulse/
├── app/
│   ├── __init__.py          # App factory
│   ├── database.py          # DB connection + BaseModel
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── url.py           # Url model
│   │   └── event.py         # Event model
│   └── routes/
│       ├── users.py         # User CRUD
│       └── url_actions/     # URL shorten/update/delete
├── .env.example
├── pyproject.toml
├── run.py
└── README.md
```
