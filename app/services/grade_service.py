from app.models.grade import Grade
from app.extensions.db import db
from sqlalchemy import func

class GradeService:
    @staticmethod
    def calculate_average(student_id):
        result = db.session.query(
            func.avg(Grade.score).label('average_score'),
            func.count(Grade.id).label('total_grades')
        ).filter_by(student_id=student_id).first()
        
        return {
            'student_id': student_id,
            'average_score': round(float(result.average_score or 0), 2),
            'total_grades': result.total_grades
        }
    
    @staticmethod
    def get_subject_average(student_id, subject):
        result = db.session.query(
            func.avg(Grade.score).label('subject_average')
        ).filter_by(student_id=student_id, subject=subject).first()
        
        return {
            'student_id': student_id,
            'subject': subject,
            'subject_average': round(float(result.subject_average or 0), 2)
        }