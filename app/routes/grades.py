from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.grade import Grade
from app.models.student import Student

grades_bp = Blueprint('grades', __name__)

@grades_bp.route('', methods=['GET'])
@jwt_required()
def get_grades():
    """Get all grades with optional filtering"""
    student_id = request.args.get('student_id')
    subject = request.args.get('subject')
    term = request.args.get('term')
    year = request.args.get('year')
    
    query = Grade.query
    
    # Apply filters
    if student_id: 
        query = query.filter_by(student_id=student_id)
    if subject:
        query = query.filter_by(subject=subject)
    if term:
        query = query.filter_by(term=term)
    if year:
        query = query.filter_by(year=int(year))
    
    grades = query.all()
    return jsonify({
        'count': len(grades),
        'grades': [grade.to_dict() for grade in grades]
    }), 200

@grades_bp.route('/<int:grade_id>', methods=['GET'])
@jwt_required()
def get_grade(grade_id):
    """Get a single grade by ID"""
    grade = Grade.query.get(grade_id)
    
    if not grade:
        return jsonify({'error': 'Grade not found'}), 404
    
    return jsonify({'grade': grade.to_dict()}), 200

@grades_bp.route('', methods=['POST'])
@jwt_required()
def create_grade():
    """Create a new grade record"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['student_id', 'subject', 'score', 'term', 'year']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verify student exists
    student = Student.query.get(data['student_id'])
    if not student: 
        return jsonify({'error': 'Student not found'}), 404
    
    try:
        # Create new grade
        grade = Grade(
            student_id=data['student_id'],
            subject=data['subject'],
            score=float(data['score']),
            max_score=float(data.get('max_score', 100.0)),
            term=data['term'],
            year=int(data['year']),
            remarks=data.get('remarks')
        )
        
        db.session.add(grade)
        db.session.commit()
        
        return jsonify({
            'message': 'Grade created successfully',
            'grade': grade.to_dict()
        }), 201
    except ValueError:
        return jsonify({'error': 'Invalid numeric value for score, max_score, or year'}), 400
    except Exception as e: 
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grades_bp.route('/<int:grade_id>', methods=['PUT'])
@jwt_required()
def update_grade(grade_id):
    """Update an existing grade"""
    grade = Grade.query.get(grade_id)
    
    if not grade:
        return jsonify({'error': 'Grade not found'}), 404
    
    data = request.get_json()
    
    try:
        # Update fields if provided
        if 'subject' in data:
            grade.subject = data['subject']
        if 'score' in data: 
            grade.score = float(data['score'])
        if 'max_score' in data: 
            grade.max_score = float(data['max_score'])
        if 'term' in data:
            grade.term = data['term']
        if 'year' in data:
            grade.year = int(data['year'])
        if 'remarks' in data:
            grade.remarks = data['remarks']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Grade updated successfully',
            'grade': grade.to_dict()
        }), 200
    except ValueError:
        return jsonify({'error': 'Invalid numeric value'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grades_bp.route('/<int:grade_id>', methods=['DELETE'])
@jwt_required()
def delete_grade(grade_id):
    """Delete a grade"""
    grade = Grade.query.get(grade_id)
    
    if not grade:
        return jsonify({'error': 'Grade not found'}), 404
    
    try:
        db.session.delete(grade)
        db.session.commit()
        return jsonify({'message': 'Grade deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grades_bp.route('/student/<int:student_id>/summary', methods=['GET'])
@jwt_required()
def get_student_grade_summary(student_id):
    """Get grade summary for a student"""
    student = Student.query.get(student_id)
    
    if not student: 
        return jsonify({'error': 'Student not found'}), 404
    
    grades = Grade.query.filter_by(student_id=student_id).all()
    
    if not grades:
        return jsonify({
            'student': student.to_dict(),
            'summary': {
                'total_subjects': 0,
                'average_score': 0,
                'average_percentage': 0
            },
            'grades': []
        }), 200
    
    # Calculate summary
    total_percentage = sum(grade.get_percentage() for grade in grades)
    average_percentage = total_percentage / len(grades)
    
    return jsonify({
        'student': student.to_dict(),
        'summary': {
            'total_subjects': len(grades),
            'average_percentage': round(average_percentage, 2)
        },
        'grades': [grade.to_dict() for grade in grades]
    }), 200