import pytest
from peewee import SqliteDatabase

from app import create_app
from app.database import db


@pytest.fixture()
def app():
    """Create a Flask application instance for testing.

    Uses an in-memory SQLite database so tests run without PostgreSQL.
    The CI workflow also provides a real PostgreSQL service container
    for integration tests if needed.
    """
    test_db = SqliteDatabase(":memory:")
    app = create_app()
    app.config.update({"TESTING": True})

    # Swap in the test database
    db.initialize(test_db)
    test_db.connect()

    yield app

    test_db.close()


@pytest.fixture()
def client(app):
    """Provide a Flask test client."""
    return app.test_client()
