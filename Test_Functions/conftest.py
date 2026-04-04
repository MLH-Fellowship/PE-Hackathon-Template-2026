"""
Pytest fixtures for URL Shortener tests.
Includes automatic schema comparison between production and test databases.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.database import db


def get_schema_structure(schema_name):
    """Get the structure of all tables in a schema."""
    query = """
        SELECT table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = %s
        ORDER BY table_name, ordinal_position;
    """
    cursor = db.execute_sql(query, (schema_name,))
    return cursor.fetchall()


def compare_schemas():
    """Compare public and test schemas, return differences."""
    public_structure = get_schema_structure('public')
    test_structure = get_schema_structure('test')

    # Create dicts keyed by (table, column)
    public_dict = {(row[0], row[1]): row for row in public_structure}
    test_dict = {(row[0], row[1]): row for row in test_structure}

    public_keys = set(public_dict.keys())
    test_keys = set(test_dict.keys())

    # Find missing columns
    in_public_only = public_keys - test_keys
    in_test_only = test_keys - public_keys
    in_both = public_keys & test_keys

    # Find type mismatches
    type_mismatches = []
    for key in in_both:
        pub_type = public_dict[key][2]  # data_type
        test_type = test_dict[key][2]
        if pub_type != test_type:
            type_mismatches.append((key[0], key[1], pub_type, test_type))

    return {
        'public_only': [(public_dict[k][0], public_dict[k][1], public_dict[k][2]) for k in sorted(in_public_only)],
        'test_only': [(test_dict[k][0], test_dict[k][1], test_dict[k][2]) for k in sorted(in_test_only)],
        'type_mismatches': type_mismatches,
        'match': len(in_public_only) == 0 and len(in_test_only) == 0 and len(type_mismatches) == 0
    }


@pytest.fixture(scope="session", autouse=True)
def check_schema_similarity():
    """
    Automatically runs before any tests.
    Compares production (public) and test schemas.
    """
    app = create_app()

    with app.app_context():
        db.connect(reuse_if_open=True)

        print("\n")
        print("=" * 60)
        print("DATABASE SCHEMA CHECK")
        print("=" * 60)

        try:
            differences = compare_schemas()

            if differences['match']:
                print("[OK] Results for similar database")
                print("     Production and Test schemas are identical.")
            else:
                print("[!!] SCHEMA DIFFERENCES DETECTED")
                print("-" * 60)

                if differences['public_only']:
                    print("\n  Columns in PRODUCTION but not in TEST:")
                    for item in differences['public_only']:
                        table, column, dtype = item
                        print(f"    - {table}.{column} ({dtype})")

                if differences['test_only']:
                    print("\n  Columns in TEST but not in PRODUCTION:")
                    for item in differences['test_only']:
                        table, column, dtype = item
                        print(f"    - {table}.{column} ({dtype})")

                if differences['type_mismatches']:
                    print("\n  Type mismatches:")
                    for table, column, pub_type, test_type in differences['type_mismatches']:
                        print(f"    - {table}.{column}: prod={pub_type}, test={test_type}")

                print("\n  [!] Consider syncing schemas before running tests.")

        except Exception as e:
            print(f"[!!] Schema check failed: {e}")
            print("     Make sure test schema exists in Supabase.")

        print("=" * 60)
        print()

        if not db.is_closed():
            db.close()

    yield  # Run tests

    # Cleanup after all tests (optional)
    print("\n")
    print("=" * 60)
    print("TEST SESSION COMPLETE")
    print("=" * 60)


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def db_connection(app):
    """Ensure database connection is available."""
    with app.app_context():
        db.connect(reuse_if_open=True)
        yield db
        if not db.is_closed():
            db.close()


@pytest.fixture
def sample_user(client):
    """Create a sample user for testing and return their data."""
    import time
    timestamp = int(time.time() * 1000)

    response = client.post('/users', json={
        'username': f'testuser_{timestamp}',
        'email': f'testuser_{timestamp}@test.com'
    })

    return response.get_json()


@pytest.fixture
def sample_url(client, sample_user):
    """Create a sample URL for testing and return its data."""
    import time
    timestamp = int(time.time() * 1000)

    response = client.post('/shorten', json={
        'user_id': sample_user['id'],
        'original_url': f'https://example.com/test/{timestamp}',
        'title': f'Test URL {timestamp}'
    })

    return response.get_json()
