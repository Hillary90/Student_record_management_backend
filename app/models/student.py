from app.extensions.db import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    student_class = db.Column(db.String(20), nullable=False)

    grades = db.relationship("Grade", backref="student", lazy=True)
