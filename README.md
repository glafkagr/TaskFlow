# 🚀 TaskFlow - Project Management Tool

TaskFlow is a full-featured **project management application** built with **Flask**.

It allows users to manage **projects, tasks, comments, and file attachments**, with **real-time updates** and **email reminders**.

---

## ✨ Features

- 🔐 **User Authentication**
  - JWT for API
  - Flask-Login for Web

- 📁 **Project Management**
  - Full CRUD operations

- ✅ **Task Management**
  - Status tracking:
    - Pending
    - In Progress
    - Completed
  - Priority levels:
    - Low
    - Medium
    - High
    - Urgent

- 💬 **Task Comments**
  - Real-time posting

- 📎 **File Attachments**
  - Upload / Download / Delete

- 🎯 **Drag & Drop**
  - Move tasks between status columns

- 📧 **Email Reminders**
  - Powered by Celery + Redis
  - Mailtrap integration

- 🛡️ **Rate Limiting**
  - Authentication endpoints protection

- 🔌 **RESTful API**
  - Flask-Smorest
  - Swagger UI Documentation

- 🧪 **Testing**
  - Full pytest test suite
  - 16 passing tests

- 🐳 **Docker Support**
  - PostgreSQL
  - Redis
  - Celery workers

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Flask, Flask-Smorest, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Login |
| **Database** | PostgreSQL (production), SQLite (development) |
| **Queue** | Celery, Redis |
| **Frontend** | Jinja2, HTMX, AlpineJS, Tailwind CSS |
| **Testing** | pytest, pytest-flask |
| **Deployment** | Docker, Docker Compose |
| **Email** | Mailtrap |

---

## 🌸 Monitoring with Flower

Flower provides a web interface to monitor **Celery tasks and workers**.

### Access Flower Dashboard

```bash
http://localhost:5555
```

### Features

- View task history and status
- Monitor worker statistics
- Track task arguments and results
- Retry failed tasks

---

## 📋 Prerequisites

Before running the project, make sure you have installed:

- Docker
- Docker Compose
- Python **3.12+** (for local development)

---

## 🚀 Quick Start with Docker

### 1. Clone the repository

```bash
git clone https://github.com/glafkagr/TaskFlow.git
cd TaskFlow
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your Mailtrap credentials (optional).

### 3. Build and run containers

```bash
docker compose up --build
```

### 4. Run tests

```bash
docker exec -it taskflow-web-1 pytest -v
```

---

## 🌐 Access the Application

Open in browser:

```text
http://localhost:5000
```

Swagger API Docs:

```text
http://localhost:5000/api/docs/swagger
```

Flower Dashboard:

```text
http://localhost:5555
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | `/api/v1/auth/register` | User registration |
| POST | `/api/v1/auth/login` | User login (returns JWT) |

### Projects

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | `/api/v1/projects/` | List user projects |
| POST | `/api/v1/projects/` | Create project |
| PUT | `/api/v1/projects/<id>` | Update project |
| DELETE | `/api/v1/projects/<id>` | Delete project |

### Tasks

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | `/api/v1/tasks/` | List tasks |
| POST | `/api/v1/tasks/` | Create task |
| PUT | `/api/v1/tasks/<id>` | Update task |
| DELETE | `/api/v1/tasks/<id>` | Delete task |

### Comments & Attachments

| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | `/api/v1/tasks/<id>/comments/` | Add comment |
| POST | `/api/v1/tasks/<id>/attachments/` | Upload attachment |

---

## 🖥️ Web Routes

| Route | Description |
|--------|-------------|
| `/` | Homepage |
| `/register` | User registration |
| `/login` | User login |
| `/dashboard` | Projects dashboard |
| `/project/<id>` | Project detail with tasks |
| `/logout` | Logout |

---

## 📂 Project Structure

```text
TaskFlow/
├── app/
│   ├── api/                # REST API endpoints
│   ├── models/             # SQLAlchemy models
│   ├── templates/          # Jinja2 templates
│   ├── web/                # Web routes (Flask-Login)
│   ├── __init__.py         # App factory
│   ├── celery_worker.py
│   ├── extensions.py
│   └── tasks.py            # Celery tasks
│
├── tests/                  # pytest test suite
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── config.py
└── wsgi.py
```

---

## 🧪 Testing

### Run tests inside Docker

```bash
docker exec -it taskflow-web-1 pytest -v
```

### Run tests locally

```bash
pytest -v
```

---

## ⚙️ Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=postgresql://taskflow:taskflow123@postgres:5432/taskflow
MAIL_USERNAME=your_mailtrap_username
MAIL_PASSWORD=your_mailtrap_password
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

---

## 💻 Local Development (Without Docker)

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run database migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Start application

```bash
python wsgi.py
```

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**glafkagr**
