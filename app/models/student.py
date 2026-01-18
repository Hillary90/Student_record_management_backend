from app import db
from datetime import datetime

class Student(db.Model):
    """Student model"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    admission_number = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    guardian_name = db.Column(db.String(200), nullable=True)
    guardian_phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with grades
    grades = db.relationship('Grade', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_grades=False):
        """Convert student object to dictionary"""
        data = {
            'id': self.id,
            'admission_number': self.admission_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender':  self.gender,
            'class_name': self.class_name,
            'email': self. email,
            'phone': self.phone,
            'address':  self.address,
            'guardian_name': self.guardian_name,
            'guardian_phone':  self.guardian_phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self. updated_at.isoformat()
        }
        
        if include_grades:
            data['grades'] = [grade.to_dict() for grade in self.grades]
        
        return data
    
    def __repr__(self):
        return f'<Student {self.admission_number}:  {self.first_name} {self.last_name}>'