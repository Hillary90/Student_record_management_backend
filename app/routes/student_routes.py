from flask import Blueprint, request, jsonify
from app.models.student import Student, db

student_bp = Blueprint("students", __name__)

@student_bp.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json()
    student = Student(
        name=data["name"],
        admission_number=data["admission_number"],
        class_name=data["class_name"]
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201

@student_bp.route("/api/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])

@student_bp.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict())