"""Peewee migrations -- create users, urls, and events tables."""

import peewee as pw
from peewee_migrate import Migrator


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.sql(
        """
        CREATE TABLE IF NOT EXISTS "user" (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
    )
    migrator.sql(
        """
        CREATE TABLE IF NOT EXISTS url (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES "user" (id),
            short_code VARCHAR(12) NOT NULL UNIQUE,
            original_url TEXT NOT NULL,
            title VARCHAR(255),
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
    )
    migrator.sql("CREATE INDEX IF NOT EXISTS url_short_code_idx ON url (short_code);")
    migrator.sql(
        """
        CREATE TABLE IF NOT EXISTS event (
            id SERIAL PRIMARY KEY,
            url_id INTEGER NOT NULL REFERENCES url (id),
            user_id INTEGER NOT NULL REFERENCES "user" (id),
            event_type VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            details TEXT
        );
        """
    )


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.sql("DROP TABLE IF EXISTS event;")
    migrator.sql("DROP TABLE IF EXISTS url;")
    migrator.sql('DROP TABLE IF EXISTS "user";')
