# TaskFlow - Project Management Tool

TaskFlow is a full-featured project management application built with Flask. It allows users to manage projects, tasks, comments, and file attachments with real-time updates and email reminders.

## Features

- **User Authentication** (JWT for API, Flask-Login for Web)
- **Project Management** (CRUD operations)
- **Task Management** with status (Pending/In Progress/Completed) and priority (Low/Medium/High/Urgent)
- **Comments** on tasks with real-time posting
- **File Attachments** (upload/download/delete)
- **Drag & Drop** tasks between status columns
- **Email Reminders** via Celery + Redis (Mailtrap integration)
- **Rate Limiting** on authentication endpoints
- **RESTful API** with Flask-Smorest (Swagger UI documentation)
- **Full Test Suite** with pytest (16 passing tests)
- **Docker** containerization with PostgreSQL, Redis, and Celery

## Monitoring with Flower

Flower provides a web interface to monitor Celery tasks and workers.

```bash
# Access Flower dashboard
http://localhost:5555
Features:

View task history and status

Monitor worker statistics

Track task arguments and results

Retry failed tasks



## Tech Stack

| Category | Technologies |
|----------|-------------|
| Backend | Flask, Flask-Smorest, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Login |
| Database | PostgreSQL (production), SQLite (development) |
| Queue | Celery, Redis |
| Frontend | Jinja2, HTMX, AlpineJS, Tailwind CSS |
| Testing | pytest, pytest-flask |
| Deployment | Docker, docker-compose |
| Email | Mailtrap (development) |

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)

## Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/yourusername/TaskFlow.git
cd TaskFlow

# Copy environment variables
cp .env.example .env
# Edit .env with your Mailtrap credentials (optional)

# Build and run
docker compose up --build

# Run tests
docker exec -it taskflow-web-1 pytest -v


Access the application at http://localhost:5000

API Endpoints
Method  Endpoint    Description
POST    /api/v1/auth/register   User registration
POST    /api/v1/auth/login  User login (returns JWT)
GET /api/v1/projects/   List user projects
POST    /api/v1/projects/   Create project
PUT /api/v1/projects/<id>   Update project
DELETE  /api/v1/projects/<id>   Delete project
GET /api/v1/tasks/  List tasks (filter by status/project)
POST    /api/v1/tasks/  Create task
PUT /api/v1/tasks/<id>  Update task
DELETE  /api/v1/tasks/<id>  Delete task
POST    /api/v1/tasks/<id>/comments/    Add comment
POST    /api/v1/tasks/<id>/attachments/ Upload attachment
API documentation available at http://localhost:5000/api/docs/swagger

Web Routes
Route   Description
/   Homepage
/register   User registration
/login  User login
/dashboard  Projects dashboard
/project/<id>   Project detail with tasks
/logout Logout
Project Structure
text
TaskFlow/
├── app/
│   ├── api/           # REST API endpoints
│   ├── models/        # SQLAlchemy models
│   ├── templates/     # Jinja2 templates
│   ├── web/           # Web routes (Flask-Login)
│   ├── __init__.py    # App factory
│   ├── celery_worker.py
│   ├── extensions.py
│   └── tasks.py       # Celery tasks
├── tests/             # pytest test suite
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── config.py
└── wsgi.py
Testing
bash
# Run tests inside Docker
docker exec -it taskflow-web-1 pytest -v

# Run tests locally (with SQLite)
pytest -v
Environment Variables
Create a .env file based on .env.example:

bash
DATABASE_URL=postgresql://taskflow:taskflow123@postgres:5432/taskflow
MAIL_USERNAME=your_mailtrap_username
MAIL_PASSWORD=your_mailtrap_password
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
Development
Local Setup (without Docker)
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python wsgi.py
Screenshots
Dashboard   Project Detail
(Add screenshot here)   (Add screenshot here)
License
MIT

Author
[glafkagr] - [https://github.com/glafkagr]
