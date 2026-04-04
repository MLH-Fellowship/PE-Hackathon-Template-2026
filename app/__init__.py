from dotenv import load_dotenv
from flask import Flask, jsonify

from app.database import init_db
from app.routes import register_routes


def create_app():
    load_dotenv()

    app = Flask(__name__)

    # 1. Initialize DB
    init_db(app)

    # 2. Import models (VERY IMPORTANT)
    from app.models.users import User
    from app.models.urls import Url
    from app.models.events import Event

    # 3. CREATE TABLES HERE 👇
    with db.connection_context():
        db.create_tables([User, Url, Event], safe=True)

    # 4. Register routes
    register_routes(app)

    # 5. Health endpoint
    @app.route("/health")
    def health():
        return jsonify(status="ok"), 200

    return app
