def register_routes(app):
    from app.routes.urls import urls_bp

    app.register_blueprint(urls_bp)
