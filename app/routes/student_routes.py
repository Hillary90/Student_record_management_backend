from flask import Blueprint, request, jsonify
from app.models.student import Student
from app.extensions.db import db

student_bp = Blueprint("students", __name__)

@student_bp.route("/", methods=["POST"])
def create_student():
    data = request.get_json()
    student = Student(**data)
    db.session.add(student)
    db.session.commit()
    return jsonify(message="Student created"), 201

@student_bp.route("/", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([s.admission_number for s in students])
