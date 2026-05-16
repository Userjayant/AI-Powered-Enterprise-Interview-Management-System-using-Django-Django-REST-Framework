# AI-Powered Enterprise Interview Management System using Django & Django REST Framework

A production-style AI-powered recruitment and interview management platform built using **Django**, **Django REST Framework**, and **Bootstrap 5**.  
This system simulates a real-world corporate hiring workflow with role-based dashboards, candidate tracking, interview scheduling, feedback management, analytics, and REST APIs.

---

# Project Overview

The application is designed to streamline and automate the hiring process inside modern organizations.

The platform allows:

- HR/Admins to manage recruitment workflows
- Interviewers to conduct evaluations
- Candidates to track applications and interviews

The system includes:
- Role-based authentication
- Resume management
- Interview scheduling
- Feedback & scoring
- Analytics dashboard
- REST APIs
- AI-powered resume screening

---

# Features

## Authentication & Authorization
- Custom User Model
- Role-Based Access Control
- Secure Login & Logout
- Password Reset System
- Profile Management

## Candidate Management
- Add/Edit/Delete Candidates
- Resume Upload (PDF/DOC)
- Skills & Experience Tracking
- Application Status Tracking
- Job Role Assignment

## Interview Management
- Schedule Interviews
- Multiple Interview Rounds
- Assign Interviewers
- Interview Status Tracking
- Calendar-Based Workflow

## Feedback & Evaluation
- Technical Evaluation
- Communication Assessment
- Problem Solving Score
- Recommendation System
- Final Hiring Decision

## Dashboard & Analytics
- HR Dashboard
- Interviewer Dashboard
- Candidate Dashboard
- Recruitment Analytics
- Charts & Reports

## AI Resume Screening
- Resume Keyword Extraction
- Skill Matching
- AI Resume Score Generation

## REST APIs
- Candidate APIs
- Interview APIs
- Feedback APIs
- Authentication APIs

---

# Tech Stack

## Backend
- Django
- Django REST Framework (DRF)

## Frontend
- Bootstrap 5
- HTML5
- CSS3
- JavaScript

## Database
- SQLite (Development)
- PostgreSQL Compatible Structure

## Additional Libraries
- django-filter
- Pillow
- python-dotenv
- SimpleJWT

---

# Current Project Structure

```bash
NEW_INTERVIEW_SYSTEM/

├── manage.py
├── db.sqlite3
├── requirements.txt
├── logs/
├── media/
├── static/
├── templates/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── migrations/
│   ├── templates/accounts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── candidates/
│   ├── migrations/
│   ├── templates/candidates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── interviews/
│   ├── migrations/
│   ├── templates/interviews/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── dashboard/
│   ├── templates/dashboard/
│   ├── views.py
│   └── urls.py
│
├── api/
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
```

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/Userjayant/AI-Powered-Enterprise-Interview-Management-System-using-Django-Django-REST-Framework.git
```

---

## Navigate to Project

```bash
cd NEW_INTERVIEW_SYSTEM
```

---

## Create Virtual Environment

```bash
python -m venv env
```

---

## Activate Virtual Environment

### Windows

```bash
env\Scripts\activate
```

### Linux / Mac

```bash
source env/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Run Development Server

```bash
python manage.py runserver
```

---

# API Modules

The project includes REST APIs for:

- Authentication
- Candidates
- Interviews
- Feedback
- Recruitment Workflow

---

# Future Enhancements

- AI-based Candidate Ranking
- Resume Parsing using NLP
- Real-Time Notifications
- Video Interview Integration
- Email Automation
- Interview Analytics Dashboard
- PostgreSQL Deployment
- Docker Support
- CI/CD Integration

---

# Screenshots

Screenshots will be added after UI completion.

---

# Project Status

Project is currently under active development.

---

# Author

## Jayant Thevarakonda

B.Tech Artificial Intelligence  
Full Stack Django Developer  
AI & Web Development Enthusiast

---

# License

This project is developed for educational and internship assessment purposes.
