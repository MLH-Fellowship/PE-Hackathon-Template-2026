"""Peewee migrations -- create urls table."""

import peewee as pw
from peewee_migrate import Migrator


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.sql(
        """
        CREATE TABLE IF NOT EXISTS url (
            id SERIAL PRIMARY KEY,
            original_url TEXT NOT NULL,
            short_code VARCHAR(12) NOT NULL UNIQUE,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            visits INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    migrator.sql("CREATE INDEX IF NOT EXISTS url_short_code_idx ON url (short_code);")


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.sql("DROP TABLE IF EXISTS url;")
