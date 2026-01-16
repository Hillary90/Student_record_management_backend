from flask import Blueprint, request, jsonify
from app.models.grade import Grade
from app.services.grade_service import GradeService
from app.extensions.db import db

grade_bp = Blueprint("grades", __name__)

@grade_bp.route("/", methods=["POST"])
def add_grade():
    data = request.get_json()
    grade = Grade(**data)
    db.session.add(grade)
    db.session.commit()
    return jsonify({"message": "Grade added", "id": grade.id}), 201

@grade_bp.route("/<int:grade_id>", methods=["PUT"])
def update_grade(grade_id):
    data = request.get_json()
    grade = Grade.query.get_or_404(grade_id)
    grade.score = data.get('score', grade.score)
    db.session.commit()
    return jsonify({"message": "Grade updated"})

@grade_bp.route("/student/<int:student_id>", methods=["GET"])
def get_student_grades(student_id):
    grades = Grade.query.filter_by(student_id=student_id).all()
    return jsonify([grade.to_dict() for grade in grades])

@grade_bp.route("/student/<int:student_id>/average", methods=["GET"])
def get_student_average(student_id):
    average_data = GradeService.calculate_average(student_id)
    return jsonify(average_data)

@grade_bp.route("/student/<int:student_id>/subject/<subject>", methods=["GET"])
def get_subject_grades(student_id, subject):
    grades = Grade.query.filter_by(student_id=student_id, subject=subject).all()
    return jsonify([grade.to_dict() for grade in grades])
