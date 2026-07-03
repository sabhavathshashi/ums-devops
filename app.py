from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = "super_secret_key"

# User store with hashed passwords
USERS = {
    "admin": {
        "username": "admin",
        "password_hash": generate_password_hash("admin123"),
        "name": "Administrator",
        "email": "admin@university.local"
    },
    "shashi": {
        "username": "shashi",
        "password_hash": generate_password_hash("shashi"),
        "name": "Shashi Kumar",
        "email": "shashi@university.local"
    }
}

# Mock databases
students_list = [
    {"id": 1, "name": "John Doe", "department": "Computer Science", "year": "Sophomore", "status": "Enrolled"},
    {"id": 2, "name": "Jane Smith", "department": "Mathematics", "year": "Senior", "status": "Enrolled"}
]

faculty_list = [
    {"id": 1, "name": "Dr. Alan Turing", "department": "Computer Science", "designation": "Professor"},
    {"id": 2, "name": "Dr. Grace Hopper", "department": "Software Engineering", "designation": "Associate Professor"}
]

courses_list = [
    {
        "code": "CS101", "name": "Intro to Programming", "credits": 4,
        "faculty": "Dr. Alan Turing", "department": "Computer Science"
    },
    {
        "code": "SE200", "name": "Software Engineering Principles", "credits": 3,
        "faculty": "Dr. Grace Hopper", "department": "Software Engineering"
    }
]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def get_user(username):
    if not username:
        return None
    return USERS.get(username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if username and password and user and check_password_hash(user['password_hash'], password):
            session['logged_in'] = True
            session['username'] = username
            flash('Successfully logged in.', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('auth.html', mode='login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')

        if not username or not password or not name or not email:
            flash('All fields are required for registration.', 'danger')
            return render_template('auth.html', mode='register')

        if username in USERS:
            flash('Username is already taken. Please choose another.', 'warning')
            return render_template('auth.html', mode='register')

        USERS[username] = {
            'username': username,
            'password_hash': generate_password_hash(password),
            'name': name,
            'email': email
        }
        session['logged_in'] = True
        session['username'] = username
        flash('Registration successful. You are now logged in.', 'success')
        return redirect(url_for('index'))

    return render_template('auth.html', mode='register')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    user = get_user(session.get('username'))
    if not user:
        flash('User profile not found.', 'danger')
        return redirect(url_for('login'))

    orders = [
        {"order_id": "ORD-1024", "status": "Delivered", "total": 2875, "items": ["Notebook", "Backpack"]},
        {"order_id": "ORD-1101", "status": "Processing", "total": 1599, "items": ["Course Material", "Lab Kit"]}
    ]

    return render_template('profile.html', user=user, orders=orders)


@app.route('/')
@login_required
def index():
    return render_template(
        'index.html', title='Dashboard',
        student_count=len(students_list),
        faculty_count=len(faculty_list),
        course_count=len(courses_list)
    )


@app.route('/students', methods=['GET'])
@login_required
def students():
    return render_template('students.html', students=students_list)


@app.route('/students/add', methods=['POST'])
@login_required
def add_student():
    new_id = max([s['id'] for s in students_list] + [0]) + 1
    new_student = {
        "id": new_id,
        "name": request.form.get('name'),
        "department": request.form.get('department'),
        "year": request.form.get('year'),
        "status": request.form.get('status', 'Enrolled')
    }
    students_list.append(new_student)
    flash("Student added successfully!", "success")
    return redirect(url_for('students'))


@app.route('/students/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    global students_list
    students_list = [s for s in students_list if s['id'] != id]
    flash("Student deleted successfully!", "success")
    return redirect(url_for('students'))


@app.route('/faculty', methods=['GET'])
@login_required
def faculty():
    return render_template('faculty.html', faculty=faculty_list)


@app.route('/faculty/add', methods=['POST'])
@login_required
def add_faculty():
    new_id = max([f['id'] for f in faculty_list] + [0]) + 1
    new_member = {
        "id": new_id,
        "name": request.form.get('name'),
        "department": request.form.get('department'),
        "designation": request.form.get('designation')
    }
    faculty_list.append(new_member)
    flash("Faculty added successfully!", "success")
    return redirect(url_for('faculty'))


@app.route('/faculty/delete/<int:id>', methods=['POST'])
@login_required
def delete_faculty(id):
    global faculty_list
    faculty_list = [f for f in faculty_list if f['id'] != id]
    flash("Faculty deleted successfully!", "success")
    return redirect(url_for('faculty'))


@app.route('/courses', methods=['GET'])
@login_required
def courses():
    return render_template('courses.html', courses=courses_list)


@app.route('/courses/add', methods=['POST'])
@login_required
def add_course():
    new_course = {
        "code": request.form.get('code'),
        "name": request.form.get('name'),
        "credits": request.form.get('credits'),
        "faculty": request.form.get('faculty'),
        "department": request.form.get('department')
    }
    courses_list.append(new_course)
    flash("Course added successfully!", "success")
    return redirect(url_for('courses'))


@app.route('/courses/delete/<code>', methods=['POST'])
@login_required
def delete_course(code):
    global courses_list
    courses_list = [c for c in courses_list if c['code'] != code]
    flash("Course deleted successfully!", "success")
    return redirect(url_for('courses'))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
