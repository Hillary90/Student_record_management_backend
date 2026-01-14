import os

class Config:
    # Secret key for sessions and JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")

    # Database connection (SQLite by default)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS settings (frontend dev servers)
    CORS_ORIGINS = [
        "http://localhost:5173",   # Vite default port
        "http://localhost:3000"    # React default port
    ]