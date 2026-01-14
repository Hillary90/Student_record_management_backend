from flask import Blueprint, request, jsonify
from app.services.search_service import build_student_query, paginate

search_bp = Blueprint("search", __name__)

@search_bp.get("/students/search")
def search_students():
    name = request.args.get("name")
    admission_number = request.args.get("admission_number")
    class_name = request.args.get("class")
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 10)

    query = build_student_query(name=name, admission_number=admission_number, class_name=class_name)
    result = paginate(query, page, per_page)
    return jsonify(result), 200