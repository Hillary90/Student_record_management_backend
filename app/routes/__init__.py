from .auth_routes import auth_bp
from .student_routes import student_bp
from .grade_routes import grade_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(student_bp, url_prefix="/students")
    app.register_blueprint(grade_bp, url_prefix="/grades")
