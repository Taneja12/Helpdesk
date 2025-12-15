# Helpdesk & Ticket Management System

A backend API built with Django & Django Rest Framework (DRF) for a helpdesk system. Supports users, agents, and admins with ticket management, automated escalations via Celery, and reporting.

## Features

- **Authentication**: User registration, login, and role-based access (User, Agent, Admin).
- **Ticket Management**: Create, update, assign, and track tickets.
- **Automated Escalations**: Tickets not updated within defined timelines are automatically escalated via Celery.
    - High Priority: 1 Hour
    - Medium Priority: 4 Hours
    - Low Priority: 24 Hours
- **Comments**: Threaded updates on tickets.
- **Reporting**: API endpoint for ticket statistics (opened, resolved, escalated).
- **Documentation**: Swagger/OpenAPI documentation.

## Prerequisites

- Python 3.8+
- Redis (for Celery)

## Setup Instructions

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    cd helpdesk
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

### 1. Start Django Server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

### 2. Start Celery Worker
Open a new terminal, activate venv, and run:
```bash
# Windows (requires pool=solo for simple dev/testing)
celery -A core worker --pool=solo -l info

# Production/Linux
celery -A core worker -l info
```

### 3. Start Celery Beat (Scheduler)
Open a new terminal, activate venv, and run:
```bash
celery -A core beat -l info
```

## API Documentation

- **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## API Endpoints

### Auth
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - View profile
- `GET /api/auth/users/search/` - Search users

### Tickets
- `GET /api/tickets/` - List tickets (filtered by role)
- `POST /api/tickets/` - Create ticket
- `GET /api/tickets/{id}/` - Retrieve ticket details
- `POST /api/tickets/{id}/assign/` - Assign ticket (Admin only)
- `POST /api/tickets/{id}/status/` - Update status (Agent/Admin)

### Comments
- `GET /api/tickets/{id}/comments/` - View comments
- `POST /api/tickets/{id}/comments/` - Add comment

### Reports
- `GET /api/reports/stats/` - Last 7 days statistics (Admin only)
