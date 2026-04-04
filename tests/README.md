# CI Test Suite

This folder contains tests that run automatically on GitHub Actions for every push and pull request.

## Test Structure

The CI pipeline runs two test suites:

### 1. Application Tests (`tests/`)

Basic application health checks:

| Test | Description |
|------|-------------|
| `test_health_check` | Verifies `/health` endpoint returns `{"status": "ok"}` |
| `test_404_returns_json` | Verifies non-existent routes return 404 |

### 2. Database Function Tests (`Test_Functions/`)

Tests individual API functions in isolation:

| File | Functions Tested |
|------|------------------|
| `test_user_creation.py` | `POST /users` - Create user, duplicate checks, validation |
| `test_url_creation.py` | `POST /shorten` - URL shortening, unique codes, events |
| `test_url_update.py` | `POST /update` - Field updates, validation, allowed fields |
| `test_url_delete.py` | `POST /delete` - Deletion, event cleanup, ownership |

## Database Schema Check

Before database tests run, the system automatically checks if the **production** (`public`) and **test** schemas are identical.

- **If schemas match:** `[OK] Results for similar database`
- **If schemas differ:** `[!!] SCHEMA DIFFERENCES DETECTED` with details

This ensures test results are valid and reflects the production database structure.

## Running Locally

```bash
# Run application tests
uv run pytest tests/ -v

# Run database function tests
uv run pytest Test_Functions/ -v -s

# Run all tests
uv run pytest tests/ Test_Functions/ -v
```

## CI Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`):

1. Spins up PostgreSQL container
2. Creates `public` and `test` schemas
3. Runs application tests
4. Runs database function tests with schema check
5. Reports results
