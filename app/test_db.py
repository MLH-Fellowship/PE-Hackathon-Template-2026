from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    "hackathon_db",
    host="localhost",
    port=5432,
    user="postgres",
    password="postgres",
)

try:
    db.connect()
    print("✅ Connected to database!")

    tables = db.get_tables()
    print("Tables:", tables)

    db.close()

except Exception as e:
    print("❌ Connection failed:")
    print(e)