# Student Record Management - Backend API

A Flask-based REST API for managing student records, grades, and user authentication.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Student Management**: CRUD operations for student records
- **Grade Management**: Track and manage student grades
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Security**: Password hashing with bcrypt, CORS protection
- **Testing**: Comprehensive test suite included

## Tech Stack

- **Framework**: Flask 
- **Database**: PostgreSQL with SQLAlchemy 
- **Authentication**: JWT (Flask-JWT-Extended)
- **Password Hashing**: bcrypt
- **Migrations**: Flask-Migrate
- **CORS**: Flask-CORS
- **Deployment**: Gunicorn for production

## Prerequisites

- Python 3.8+
- PostgreSQL
- pipenv

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hillary90/Student_record_management_backend.git

   cd Student_record_management_backend
   ```

2. **Install dependencies**
   ```bash
   pipenv install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run database migrations**
   ```bash
   flask db upgrade
   ```

5. **Seed the database (optional)**
   ```bash
   python seed_db.py
   ```

## Running the Application

**Development:**
```bash
python run.py
```

**Production:**
```bash
gunicorn run:app
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile (protected)

### Students
- `GET /api/students` - List all students (protected)
- `POST /api/students` - Create new student (protected)
- `GET /api/students/{id}` - Get student by ID (protected)
- `PUT /api/students/{id}` - Update student (protected)
- `DELETE /api/students/{id}` - Delete student (protected)

### Grades
- `GET /api/grades` - List all grades (protected)
- `POST /api/grades` - Create new grade (protected)
- `GET /api/grades/student/{student_id}` - Get grades for student (protected)
- `PUT /api/grades/{id}` - Update grade (protected)
- `DELETE /api/grades/{id}` - Delete grade (protected)

### Health Check
- `GET /api/health` - API health status

## Database Schema

### Users
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- created_at

### Students
- id (Primary Key)
- first_name
- last_name
- email (Unique)
- phone
- date_of_birth
- enrollment_date
- created_at
- updated_at

### Grades
- id (Primary Key)
- student_id (Foreign Key)
- subject
- grade
- semester
- academic_year
- created_at
- updated_at

## Deployment

The application is configured for deployment on Render or similar platforms:

1. Set environment variables in your hosting platform
2. Use `gunicorn run:app` as the start command
3. Ensure PostgreSQL database is configured

## Security Notes

- Change default secret keys in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Regularly update dependencies

## License

This project is licensed under the MIT License.