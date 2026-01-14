from flask import Flask
from app.extensions.db import db
from app.extensions.migrate import migrate
from app.extensions.jwt import jwt
from app.extensions.cors import cors
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    register_routes(app)

    return app
