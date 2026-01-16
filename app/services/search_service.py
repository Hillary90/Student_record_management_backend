from app.models.student import Student

def build_student_query(name=None, admission_number=None, class_name=None):
    query = Student.query
    if name:
        query = query.filter(Student.name.ilike(f"%{name.strip()}%"))
    if admission_number:
        query = query.filter(Student.admission_number == admission_number.strip())
    if class_name:
        query = query.filter(Student.class_name == class_name.strip())
    return query

def paginate(query, page=1, per_page=10):
    page = max(int(page or 1), 1)
    per_page = min(max(int(per_page or 10), 1), 100)
    items = query.order_by(Student.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": [s.to_dict() for s in items.items],
        "page": items.page,
        "per_page": items.per_page,
        "total": items.total,
        "pages": items.pages,
    }