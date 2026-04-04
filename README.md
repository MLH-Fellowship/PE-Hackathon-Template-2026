# MLH PE Hackathon — Flask + Peewee + PostgreSQL Template

A minimal hackathon starter template. You get the scaffolding and database wiring — you build the models, routes, and CSV loading logic.

**Stack:** Flask · Peewee ORM · PostgreSQL · uv

## **Important**

You need to work with around the seed files that you can find in [MLH PE Hackathon](https://mlh-pe-hackathon.com) platform. This will help you build the schema for the database and have some data to do some testing and submit your project for judging. If you need help with this, reach out on Discord or on the Q&A tab on the platform.

## Prerequisites

- **uv** — a fast Python package manager that handles Python versions, virtual environments, and dependencies automatically.
  Install it with:
  ```bash
  # macOS / Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Windows (PowerShell)
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  For other methods see the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/).
- PostgreSQL running locally (you can use Docker or a local instance)

## uv Basics

`uv` manages your Python version, virtual environment, and dependencies automatically — no manual `python -m venv` needed.

| Command | What it does |
|---------|--------------|
| `uv sync` | Install all dependencies (creates `.venv` automatically) |
| `uv run <script>` | Run a script using the project's virtual environment |
| `uv add <package>` | Add a new dependency |
| `uv remove <package>` | Remove a dependency |

## Quick Start

```bash
# 1. Clone the repo
git clone <repo-url> && cd mlh-pe-hackathon

# 2. Install dependencies
uv sync

# 3. Create the database
createdb hackathon_db

# 4. Configure environment
cp .env.example .env   # edit if your DB credentials differ

# 5. Run the server
uv run run.py

# 6. Verify
curl http://localhost:5000/health
# → {"status":"ok"}
```

## Docker Quick Start

```bash
# 1. Build images
docker compose build

# 2. Start core infrastructure
docker compose up -d db redis

# 3. Run migrations once
docker compose --profile setup run --rm migrate

# 4. Start scaled app fleet + load balancer
docker compose up -d web1 web2 web3 nginx

# 5. Verify
curl http://localhost/health
```

## VM Deployment Script (Reusable Locally)

The repository includes a reusable deployment script at [scripts/deploy-vm.sh](scripts/deploy-vm.sh).
The GitHub workflow [.github/deploy.yml](.github/deploy.yml) calls this same script over SSH on your VM.

Run it from the repo root:

```bash
chmod +x scripts/deploy-vm.sh
./scripts/deploy-vm.sh
```

## Scalability Quest (k6 + Nginx + Redis)

### Bronze (50 concurrent users)

```bash
k6 run load-tests/k6-quest.js \
    -e BASE_URL=http://localhost \
    -e VUS=50 \
    -e DURATION=2m \
    -e SHORTEN_RATIO=0.2
```

Record:
- p95 latency from http_req_duration
- error rate from http_req_failed

### Silver (200 concurrent users, scale-out)

```bash
# Proof of scale-out
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Load test
k6 run load-tests/k6-quest.js \
    -e BASE_URL=http://localhost \
    -e VUS=200 \
    -e DURATION=3m \
    -e SHORTEN_RATIO=0.2
```

Target:
- p95 under 3 seconds

### Gold (500 concurrent users + caching)

```bash
k6 run load-tests/k6-quest.js \
    -e BASE_URL=http://localhost \
    -e VUS=500 \
    -e DURATION=4m \
    -e SHORTEN_RATIO=0.15
```

Target:
- error rate under 5%

### Notes

- Traffic goes through Nginx at port 80 and is distributed across web1, web2, and web3.
- Redirect lookups are cached in Redis to cut repeated database reads.
- Keep FLASK_DEBUG disabled for load testing and production-like runs.

## Migrations (peewee-migrate)

```bash
# Apply all pending migrations
uv run scripts/migrate.py up

# Roll back the latest migration
uv run scripts/migrate.py down

# Create a new empty migration file
uv run scripts/migrate.py create add_some_change
```

## URL Shortener Endpoints

```bash
# Create a short URL
curl -X POST http://localhost:5000/shorten \
    -H "Content-Type: application/json" \
    -d '{"url":"https://example.com/some/long/path"}'

# Response
# {
#   "original_url": "https://example.com/some/long/path",
#   "short_code": "a1B2c3",
#   "short_url": "http://localhost:5000/a1B2c3"
# }

# Redirect to original URL
curl -i http://localhost:5000/a1B2c3
```

## Project Structure

```
mlh-pe-hackathon/
├── app/
│   ├── __init__.py          # App factory (create_app)
│   ├── database.py          # DatabaseProxy, BaseModel, connection hooks
│   ├── models/
│   │   └── __init__.py      # Import your models here
│   └── routes/
│       └── __init__.py      # register_routes() — add blueprints here
├── .env.example             # DB connection template
├── .gitignore               # Python + uv gitignore
├── .python-version          # Pin Python version for uv
├── pyproject.toml           # Project metadata + dependencies
├── run.py                   # Entry point: uv run run.py
└── README.md
```

## How to Add a Model

1. Create a file in `app/models/`, e.g. `app/models/product.py`:

```python
from peewee import CharField, DecimalField, IntegerField

from app.database import BaseModel


class Product(BaseModel):
    name = CharField()
    category = CharField()
    price = DecimalField(decimal_places=2)
    stock = IntegerField()
```

2. Import it in `app/models/__init__.py`:

```python
from app.models.product import Product
```

3. Create the table (run once in a Python shell or a setup script):

```python
from app.database import db
from app.models.product import Product

db.create_tables([Product])
```

## How to Add Routes

1. Create a blueprint in `app/routes/`, e.g. `app/routes/products.py`:

```python
from flask import Blueprint, jsonify
from playhouse.shortcuts import model_to_dict

from app.models.product import Product

products_bp = Blueprint("products", __name__)


@products_bp.route("/products")
def list_products():
    products = Product.select()
    return jsonify([model_to_dict(p) for p in products])
```

2. Register it in `app/routes/__init__.py`:

```python
def register_routes(app):
    from app.routes.products import products_bp
    app.register_blueprint(products_bp)
```

## How to Load CSV Data

```python
import csv
from peewee import chunked
from app.database import db
from app.models.product import Product

def load_csv(filepath):
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with db.atomic():
        for batch in chunked(rows, 100):
            Product.insert_many(batch).execute()
```

## Useful Peewee Patterns

```python
from peewee import fn
from playhouse.shortcuts import model_to_dict

# Select all
products = Product.select()

# Filter
cheap = Product.select().where(Product.price < 10)

# Get by ID
p = Product.get_by_id(1)

# Create
Product.create(name="Widget", category="Tools", price=9.99, stock=50)

# Convert to dict (great for JSON responses)
model_to_dict(p)

# Aggregations
avg_price = Product.select(fn.AVG(Product.price)).scalar()
total = Product.select(fn.SUM(Product.stock)).scalar()

# Group by
from peewee import fn
query = (Product
         .select(Product.category, fn.COUNT(Product.id).alias("count"))
         .group_by(Product.category))
```

## Tips

- Use `model_to_dict` from `playhouse.shortcuts` to convert model instances to dictionaries for JSON responses.
- Wrap bulk inserts in `db.atomic()` for transactional safety and performance.
- The template uses `teardown_appcontext` for connection cleanup, so connections are closed even when requests fail.
- Check `.env.example` for all available configuration options.
