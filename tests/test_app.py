import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['logged_in'] = True
            sess['username'] = 'admin'
        yield client


def test_login_page(client):
    with client.session_transaction() as sess:
        sess.pop('logged_in', None)
        sess.pop('username', None)
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Sign In' in response.data


def test_register_page():
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Create Account' in response.data


def test_login_authentication():
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Dashboard Overview' in response.data
        assert b'Successfully logged in.' in response.data


def test_profile_page(client):
    response = client.get('/profile')
    assert response.status_code == 200
    assert b'My Profile' in response.data
    assert b'Administrator' in response.data


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
