from app import create_app, db
from app.models.user import User
from app.models.student import Student
from app.models.grade import Grade
from datetime import datetime, date

def seed_database():
    """Seed the database with sample data"""
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Grade.query.delete()
        Student.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Create users
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@school.com',
            role='admin'
        )
        admin.set_password('admin123')
        
        print("Creating teacher user...")
        teacher = User(
            username='teacher',
            email='teacher@school.com',
            role='teacher'
        )
        teacher.set_password('teacher123')
        
        db.session.add(admin)
        db.session.add(teacher)
        db.session.commit()
        print("Users created!")
        
        # Get Student model fields
        print("Creating students...")
        from sqlalchemy import inspect
        student_mapper = inspect(Student)
        student_columns = [column.key for column in student_mapper.attrs]
        print(f"   Student model has these fields: {student_columns}")
        
        # Student data
        students_data = [
            {
                'admission_number': 'STD001',
                'first_name': 'Peter',
                'last_name': 'Mburu',
                'date_of_birth': date(2010, 5, 15),
                'gender': 'Male',
                'class_name': 'Form 3',
                'email': 'peter.mburu@gmail.com',
                'phone': '+2544567890',
                'address': '123000 Kiambu',
                'guardian_name': 'Jane Mburu',
                'guardian_phone': '+2544567800'
            },
            {
                'admission_number': 'STD002',
                'first_name': 'Sarah',
                'last_name': 'Jeptoo',
                'date_of_birth': date(2010, 8, 22),
                'gender': 'Female',
                'class_name': 'Form 2',
                'email': 'sarah.jeptoo@gmail.com',
                'phone': '+2544567891',
                'address': '456-00200 Nairobi',
                'guardian_name': 'Mike Smith',
                'guardian_phone': '+2544567801'
            },
            {
                'admission_number': 'STD003',
                'first_name': 'Michael',
                'last_name': 'Omindi',
                'date_of_birth': date(2011, 3, 10),
                'gender': 'Male',
                'class_name': 'Form 2',
                'email': 'michael.omindi@gmail.com',
                'phone': '+2544567892',
                'address': '789-00100 Mombasa',
                'guardian_name': 'Lisa Johnson',
                'guardian_phone': '+2544567802'
            },
            {
                'admission_number': 'STD004',
                'first_name': 'Emily',
                'last_name': 'Karanja',
                'date_of_birth': date(2011, 11, 5),
                'gender': 'Female',
                'class_name': 'Form 1',
                'email': 'emily.karanja@gmail.com',
                'phone': '+2544567893',
                'address': '321-00200 Nakuru',
                'guardian_name': 'Robert Brown',
                'guardian_phone': '+2544567803'
            },
            {
                'admission_number': 'STD005',
                'first_name': 'David',
                'last_name': 'Kamau',
                'date_of_birth': date(2009, 7, 18),
                'gender': 'Male',
                'class_name': 'Form 1',
                'email': 'david.kamau@gmail.com',
                'phone': '+2544567894',
                'address': '654-00300 Eldoret',
                'guardian_name': 'Mary Wilson',
                'guardian_phone': '+2544567804'
            }
        ]
        
        students = []
        for student_data in students_data: 
            # Only use fields that exist in the Student model
            filtered_data = {k: v for k, v in student_data.items() if k in student_columns}
            student = Student(**filtered_data)
            students.append(student)
            db.session.add(student)
        
        db.session.commit()
        print(f"{len(students)} students created!")
        
        # Get Grade model fields
        print("Creating grades...")
        grade_mapper = inspect(Grade)
        grade_columns = [column.key for column in grade_mapper.attrs]
        print(f"   Grade model has these fields: {grade_columns}")
        
        subjects = ['Mathematics', 'English', 'Science', 'History', 'Geography']
        current_year = datetime.now().year
        
        grades_count = 0
        for student in students: 
            for subject in subjects: 
                score_value = 85 + (hash(f"{student.id}{subject}") % 15)
                
                # Determine letter grade
                if score_value >= 90:
                    letter_grade = 'A'
                elif score_value >= 80:
                    letter_grade = 'B'
                elif score_value >= 70:
                    letter_grade = 'C'
                elif score_value >= 60:
                    letter_grade = 'D'
                else: 
                    letter_grade = 'F'
                
                # Build grade data with only valid fields
                grade_data = {
                    'student_id': student.id,
                    'subject': subject,
                    'score': score_value,
                }
                
                # Add optional fields if they exist
                if 'grade' in grade_columns:
                    grade_data['grade'] = letter_grade
                if 'term' in grade_columns:
                    grade_data['term'] = 'Term 1'
                if 'year' in grade_columns:
                    grade_data['year'] = current_year
                if 'remarks' in grade_columns:
                    grade_data['remarks'] = 'Good performance'
                if 'exam_type' in grade_columns:
                    grade_data['exam_type'] = 'Mid-Term'
                
                grade = Grade(**grade_data)
                db.session.add(grade)
                grades_count += 1
        
        db.session.commit()
        print(f"{grades_count} grades created for all students!")
        
        print("\n" + "="*60)
        print("DATABASE SEEDED SUCCESSFULLY!")
        print("="*60)
        print(f"\nSummary:")
        print(f"   • Users created: {User.query.count()} (1 admin, 1 teacher)")
        print(f"   • Students created: {Student.query.count()}")
        print(f"   • Grades created: {Grade.query.count()}")
        print(f"\nLogin Credentials:")
        print("-" * 60)
        print("Admin Account:")
        print("   Username: admin")
        print("   Password: admin123")
        print()
        print("Teacher Account:")
        print("   Username: teacher")
        print("   Password: teacher123")
        print("-" * 60)

if __name__ == '__main__':
    seed_database()