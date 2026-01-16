<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    admission_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    class_name = db.Column(db.String(50), nullable=False, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "admission_number": self.admission_number,
            "class_name": self.class_name,
        }
=======
from app.extensions.db import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    student_class = db.Column(db.String(20), nullable=False)

    grades = db.relationship("Grade", backref="student", lazy=True)
>>>>>>> dev
