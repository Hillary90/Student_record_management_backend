from flask import Blueprint, request, jsonify
from app.models.grade import Grade
from app.extensions.db import db

grade_bp = Blueprint("grades", __name__)

@grade_bp.route("/", methods=["POST"])
def add_grade():
    data = request.get_json()
    grade = Grade(**data)
    db.session.add(grade)
    db.session.commit()
    return jsonify(message="Grade added"), 201
