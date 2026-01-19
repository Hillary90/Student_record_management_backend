from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.student import Student
from datetime import datetime

students_bp = Blueprint('students', __name__)

@students_bp.route('', methods=['GET'])
@jwt_required()
def get_students():
    """Get all students with optional filtering"""
    # Query parameters for filtering
    class_name = request.args.get('class_name')
    search = request.args.get('search')
    
    query = Student.query
    
    # Filter by class
    if class_name:
        query = query.filter_by(class_name=class_name)
    
    # Search by name or admission number
    if search: 
        query = query.filter(
            db.or_(
                Student.first_name.ilike(f'%{search}%'),
                Student.last_name.ilike(f'%{search}%'),
                Student.admission_number.ilike(f'%{search}%')
            )
        )
    
    students = query.all()
    return jsonify({
        'count': len(students),
        'students': [student.to_dict() for student in students]
    }), 200

@students_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    """Get a single student by ID"""
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    include_grades = request.args.get('include_grades', 'false').lower() == 'true'
    return jsonify({'student': student.to_dict(include_grades=include_grades)}), 200

@students_bp.route('', methods=['POST'])
@jwt_required()
def create_student():
    """Create a new student"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['admission_number', 'first_name', 'last_name', 'date_of_birth', 'gender', 'class_name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if admission number already exists
    if Student.query.filter_by(admission_number=data['admission_number']).first():
        return jsonify({'error': 'Admission number already exists'}), 409
    
    try:
        # Parse date of birth
        dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        # Create new student
        student = Student(
            admission_number=data['admission_number'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=dob,
            gender=data['gender'],
            class_name=data['class_name'],
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            guardian_name=data.get('guardian_name'),
            guardian_phone=data.get('guardian_phone')
        )
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'message': 'Student created successfully',
            'student': student.to_dict()
        }), 201
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@students_bp.route('/<int:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    """Update an existing student"""
    student = Student.query.get(student_id)
    
    if not student: 
        return jsonify({'error': 'Student not found'}), 404
    
    data = request.get_json()
    
    try:
        # Update fields if provided
        if 'first_name' in data: 
            student.first_name = data['first_name']
        if 'last_name' in data:
            student.last_name = data['last_name']
        if 'date_of_birth' in data:
            student.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        if 'gender' in data:
            student.gender = data['gender']
        if 'class_name' in data: 
            student.class_name = data['class_name']
        if 'email' in data: 
            student.email = data['email']
        if 'phone' in data:
            student.phone = data['phone']
        if 'address' in data: 
            student.address = data['address']
        if 'guardian_name' in data:
            student.guardian_name = data['guardian_name']
        if 'guardian_phone' in data: 
            student.guardian_phone = data['guardian_phone']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Student updated successfully',
            'student': student.to_dict()
        }), 200
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@students_bp.route('/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    """Delete a student"""
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500