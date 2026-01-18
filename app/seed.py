from app import create_app, db
from app.models.user import User
from app.models.student import Student
from app.models.grade import Grade
from datetime import date

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(username='admin', email='admin@school.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create teacher user
        print("Creating teacher user...")
        teacher = User(username='teacher', email='teacher@school.com', role='teacher')
        teacher.set_password('teacher123')
        db.session.add(teacher)
        
        db.session. commit()
        print("Users created!")
        
        # Create students
        print("Creating students...")
        students_data = [
            {
                'admission_number': 'ADM001',
                'first_name':  'John',
                'last_name': 'Doe',
                'date_of_birth': date(2005, 6, 15),
                'gender': 'Male',
                'class_name': 'Form 1',
                'email': 'john.doe@student.school.com',
                'phone':  '+254712345678',
                'address': '123 School Street, Nairobi',
                'guardian_name': 'Jane Doe',
                'guardian_phone':  '+254787654321'
            },
            {
                'admission_number': 'ADM002',
                'first_name':  'Mary',
                'last_name': 'Smith',
                'date_of_birth':  date(2005, 8, 20),
                'gender':  'Female',
                'class_name': 'Form 1',
                'email': 'mary.smith@student.school. com',
                'phone': '+254723456789',
                'address': '456 Main Road, Nairobi',
                'guardian_name': 'Robert Smith',
                'guardian_phone': '+254798765432'
            },
            {
                'admission_number': 'ADM003',
                'first_name': 'Peter',
                'last_name': 'Johnson',
                'date_of_birth': date(2004, 3, 10),
                'gender': 'Male',
                'class_name': 'Form 2',
                'email': 'peter.johnson@student.school.com',
                'phone':  '+254734567890',
                'address': '789 Park Avenue, Nairobi',
                'guardian_name': 'Sarah Johnson',
                'guardian_phone': '+254745678901'
            },
            {
                'admission_number': 'ADM004',
                'first_name': 'Alice',
                'last_name': 'Williams',
                'date_of_birth': date(2004, 11, 5),
                'gender': 'Female',
                'class_name': 'Form 2',
                'email':  'alice.williams@student. school.com',
                'phone': '+254756789012',
                'address': '321 River Street, Nairobi',
                'guardian_name': 'Michael Williams',
                'guardian_phone': '+254767890123'
            },
            {
                'admission_number':  'ADM005',
                'first_name': 'David',
                'last_name':  'Brown',
                'date_of_birth': date(2003, 7, 22),
                'gender': 'Male',
                'class_name': 'Form 3',
                'email': 'david. brown@student.school.com',
                'phone': '+254778901234',
                'address':  '555 Hill Road, Nairobi',
                'guardian_name': 'Linda Brown',
                'guardian_phone': '+254789012345'
            },
        ]
        
        students = []
        for student_data in students_data:
            student = Student(**student_data)
            db.session.add(student)
            students.append(student)
        
        db.session.commit()
        print(f" {len(students)} students created!")
        
        # Create grades
        print("Creating grades...")
        subjects = ['Mathematics', 'English', 'Science', 'History', 'Geography']
        
        import random
        for student in students: 
            for subject in subjects: 
                score = random.randint(60, 100)
                
                grade = Grade(
                    student_id=student.id,
                    subject=subject,
                    score=score,
                    max_score=100,
                    term='Term 1',
                    year=2026,
                    remarks='Excellent work!' if score >= 90 else 'Good performance' if score >= 75 else 'Needs improvement'
                )
                db.session.add(grade)
        
        db.session.commit()
        print(f" Grades created for all students!")
        
    
if __name__ == '__main__':
    seed_database()