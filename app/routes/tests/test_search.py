import pytest
from app import create_app, db
from app.models.student import Student

@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.create_all()
        db.session.add_all([
            Student(name="Amina Yusuf", admission_number="ADM001", class_name="Form 1"),
            Student(name="Brian Otieno", admission_number="ADM002", class_name="Form 2"),
            Student(name="Cynthia Wanjiru", admission_number="ADM003", class_name="Form 1"),
        ])
        db.session.commit()
    return app.test_client()

def test_search_by_name(client):
    res = client.get("/students/search?name=Amina")
    data = res.get_json()
    assert res.status_code == 200
    assert data["total"] == 1

def test_filter_by_class(client):
    res = client.get("/students/search?class=Form 1")
    data = res.get_json()
    assert res.status_code == 200
    assert data["total"] == 2

def test_pagination(client):
    res = client.get("/students/search?page=1&per_page=2")
    data = res.get_json()
    assert res.status_code == 200
    assert data["per_page"] == 2