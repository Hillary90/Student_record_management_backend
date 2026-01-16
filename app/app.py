from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    admission_number = db.Column(db.String(20), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "admission_number": self.admission_number,
            "course": self.course,
            "created_at": self.created_at.isoformat()
        }

# Home route
@app.route("/")
def home():
    return "Student Management App is running"

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json()

    # Validate required fields
    required_fields = ["first_name", "last_name", "email", "admission_number", "course"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"{field} is required"}), 400

    student = Student(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        admission_number=data["admission_number"],
        course=data["course"]
    )

    try:
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email or admission number already exists"}), 400


@app.route("/api/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students]), 200

@app.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict()), 200

@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()

    # Optional: only update if provided
    if "first_name" in data and data["first_name"]:
        student.first_name = data["first_name"]
    if "last_name" in data and data["last_name"]:
        student.last_name = data["last_name"]
    if "email" in data and data["email"]:
        student.email = data["email"]
    if "admission_number" in data and data["admission_number"]:
        student.admission_number = data["admission_number"]
    if "course" in data and data["course"]:
        student.course = data["course"]

    try:
        db.session.commit()
        return jsonify(student.to_dict()), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email or admission number already exists"}), 400

@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": f"Student {id} deleted successfully"}), 200
  
if __name__ == "__main__":
    app.run(debug=True)




