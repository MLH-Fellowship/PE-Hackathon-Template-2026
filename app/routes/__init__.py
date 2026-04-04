def register_routes(app):
    """Register all route blueprints with the Flask app."""
    from app.routes.users import users_bp
    from app.routes.url_actions import url_creation_bp, url_updated_bp, url_delete_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(url_creation_bp)
    app.register_blueprint(url_updated_bp)
    app.register_blueprint(url_delete_bp)
