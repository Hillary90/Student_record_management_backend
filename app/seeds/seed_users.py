from app import create_app
from app.extensions.db import db
from app.models.user import User

app = create_app()
with app.app_context():
    admin = User(username="admin", role="Admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
