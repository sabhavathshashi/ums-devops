# University Management System (UMS)

The University Management System (UMS) is a full-stack web application built with Python Flask, enabling university administrators, faculty, and students to manage academic operations through a unified interface.

## Technology Stack
- **Backend**: Python 3.11, Flask 3.0.3, Jinja2
- **Frontend**: HTML5, Vanilla CSS (Custom Dark Mode Glassmorphism)
- **CI/CD**: GitHub Actions (Lint, Test, Docker Build, Deploy)
- **Containerization**: Docker, Docker Hub
- **Testing & Quality**: pytest, flake8

## Features
- **Dashboard**: High-level university metrics at a glance.
- **Student Management**: View, add, delete, and filter student records.
- **Faculty Management**: Oversee teaching staff, departments, and designations.
- **Course Catalog**: Manage academic courses, credits, and faculty assignments.

## Quick Start (Local Development)

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd university-management-system
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   .\venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask development server**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open [http://localhost:5000](http://localhost:5000) in your web browser.

## Docker Deployment
```bash
# Build the Docker image
docker build -t ums-flask:dev .

# Run the container
docker run -p 5000:5000 ums-flask:dev
```

## Running Tests
```bash
# Run pytest
pytest

# Run flake8 linter
flake8 . --max-line-length=120 --exclude=venv,__pycache__
```

## CI/CD Pipeline
The automated pipeline in `.github/workflows/ci-cd.yml` performs the following actions on every push:
1. Lints the Python codebase with `flake8`.
2. Runs unit tests using `pytest`.
3. Builds the Docker image.
4. On `main` branch pushes, deploys the image to Docker Hub.