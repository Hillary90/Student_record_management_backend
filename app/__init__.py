from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from app.config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from app.routes. auth import auth_bp
    from app.routes.students import students_bp
    from app.routes. grades import grades_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(grades_bp, url_prefix='/api/grades')
    
    # Health check route
    @app.route('/api/health')
    def health_check():
        return {'status':  'healthy', 'message': 'Student Record Management API is running'}, 200
    
    return app