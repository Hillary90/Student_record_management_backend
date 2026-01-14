from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register only your search blueprint
    from app.routes.search_routes import search_bp
    app.register_blueprint(search_bp)

    return app