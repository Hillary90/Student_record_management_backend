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