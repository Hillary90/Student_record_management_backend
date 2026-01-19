from app import db
from datetime import datetime

class Grade(db.Model):
    """Grade model for student academic records"""
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, default=100.0)
    term = db.Column(db.String(50), nullable=False, default='Term 1')  
    year = db.Column(db.Integer, nullable=False, default=2024)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_percentage(self):
        """Calculate percentage score"""
        return (self.score / self.max_score) * 100 if self.max_score > 0 else 0
    
    def get_grade_letter(self):
        """Calculate letter grade based on percentage"""
        percentage = self.get_percentage()
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else: 
            return 'F'
    
    def to_dict(self):
        """Convert grade object to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'score': self.score,
            'max_score': self.max_score,
            'percentage': round(self.get_percentage(), 2),
            'grade_letter': self.get_grade_letter(),
            'term': self.term,
            'year': self.year,
            'remarks': self.remarks,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Grade {self.subject}: {self.score}/{self.max_score}>'