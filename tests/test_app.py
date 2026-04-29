import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Dashboard Overview' in response.data


def test_students_page(client):
    response = client.get('/students')
    assert response.status_code == 200
    assert b'Student Management' in response.data


def test_faculty_page(client):
    response = client.get('/faculty')
    assert response.status_code == 200
    assert b'Faculty Management' in response.data


def test_courses_page(client):
    response = client.get('/courses')
    assert response.status_code == 200
    assert b'Course Catalog' in response.data
