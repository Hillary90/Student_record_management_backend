from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return {"error": "No data provided"}, 400

    if User.query.filter_by(email=data.get("email")).first():
        return {"error": "Email already exists"}, 400

    user = User(
        username=data.get("username"),
        email=data.get("email"),
        role=data.get("role", "student")
    )
    user.set_password(data.get("password"))

    db.session.add(user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return {"error": "Email and password required"}, 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=user.id)

    return {"access_token": access_token}, 200
