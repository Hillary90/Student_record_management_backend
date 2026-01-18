import os
from app import create_app, db

# Determine environment:  production on Render, development locally
env = os.getenv('FLASK_ENV') or os.getenv('RENDER') and 'production' or 'development'

# Create Flask application
app = create_app(env)

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    from app. models import User, Student, Grade
    return {
        'db':  db,
        'User':  User,
        'Student': Student,
        'Grade': Grade
    }

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db. create_all()
    
    app.run(host='0.0.0.0', port=5000, debug=True)