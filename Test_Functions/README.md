# Test Suite - URL Shortener

This folder contains pytest tests for testing individual functions in isolation.

## Prerequisites

Make sure dependencies are installed:
```bash
uv sync
```

## Running Tests

### Run All Tests
```bash
uv run pytest Test_Functions/ -v
```

### Run Specific Test File
```bash
uv run pytest Test_Functions/test_user_creation.py -v
uv run pytest Test_Functions/test_url_creation.py -v
uv run pytest Test_Functions/test_url_update.py -v
uv run pytest Test_Functions/test_url_delete.py -v
```

### Run Specific Test Function
```bash
uv run pytest Test_Functions/test_user_creation.py::test_create_user_success -v
```

### Run with Coverage Report
```bash
uv run pytest Test_Functions/ --cov=app --cov-report=html
```

## Test Files

| File | Description |
|------|-------------|
| `conftest.py` | Shared fixtures (Flask app, test client, database setup) |
| `test_user_creation.py` | Tests for user registration endpoint |
| `test_url_creation.py` | Tests for URL shortening endpoint |
| `test_url_update.py` | Tests for URL update endpoint |
| `test_url_delete.py` | Tests for URL deletion endpoint |

## Test Options

| Flag | Description |
|------|-------------|
| `-v` | Verbose output |
| `-vv` | More verbose output |
| `--tb=short` | Shorter traceback |
| `-x` | Stop on first failure |
| `-k "keyword"` | Run tests matching keyword |

## Example Output

```
========================= test session starts ==========================
collected 12 items

test_user_creation.py::test_create_user_success PASSED
test_user_creation.py::test_create_user_missing_fields PASSED
test_user_creation.py::test_create_user_duplicate_username PASSED
...

========================= 12 passed in 2.34s ===========================
```
