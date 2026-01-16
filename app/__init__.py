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

    # ✅ Import models so Alembic sees them
    from app.models import student

    # Register blueprints
    from app.routes.search_routes import search_bp
    from app.routes.student_routes import student_bp
    app.register_blueprint(search_bp)
    app.register_blueprint(student_bp)

    return app