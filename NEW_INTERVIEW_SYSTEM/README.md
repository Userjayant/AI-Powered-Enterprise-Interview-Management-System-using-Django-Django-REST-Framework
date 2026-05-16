# 💼 InterviewIQ — AI-Powered Interview Management System

A production-quality Django + DRF recruitment platform with role-based access, AI resume scoring, analytics dashboard, and full interview lifecycle management.

---

## 🚀 Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create logs folder
mkdir -p logs static

# 4. Apply migrations
python manage.py makemigrations accounts candidates interviews
python manage.py migrate

# 5. Seed demo data (creates all demo users + sample data)
python seed_data.py

# 6. Run server
python manage.py runserver
```

Open **http://127.0.0.1:8000**

---

## 🔐 Demo Login Accounts

| Role        | Email                    | Password   |
|-------------|--------------------------|------------|
| HR Admin    | hr@demo.com              | demo1234   |
| Interviewer | interviewer@demo.com     | demo1234   |
| Candidate   | candidate@demo.com       | demo1234   |
| Superuser   | admin@demo.com           | admin1234  |

---

## 🏗️ Architecture

```
NEW_INTERVIEW_SYSTEM/
├── config/            # Django settings, URLs, WSGI/ASGI
├── accounts/          # Custom User model, login, register, profile
├── candidates/        # JobRole + Candidate models, AI scoring
├── interviews/        # Interview scheduling + feedback
├── dashboard/         # Role-specific analytics dashboards
├── api/               # Django REST Framework endpoints
├── templates/         # Global base.html + per-app templates
├── static/            # CSS, JS, images
├── media/             # Uploaded files (resumes, profile images)
├── logs/              # Application logs
├── seed_data.py       # Demo data seeder
└── requirements.txt
```

---

## ✨ Features

### HR Admin
- 📊 Analytics dashboard with Chart.js (pipeline, trends, department breakdown)
- 👥 Full candidate management (CRUD + status pipeline)
- 💼 Job role creation and management
- 📅 Interview scheduling with email notifications
- 👷 Staff management (create Interviewer/HR accounts)
- 🤖 AI Resume Score (keyword matching + experience weighting)
- 🔍 Search & filter candidates by status, role, skills

### Interviewer
- 📋 View assigned interviews
- ✅ Submit structured feedback with 4-dimension scoring
- 📈 Track average scores and pending feedback

### Candidate
- 📝 Self-registration and profile management
- 📄 Resume upload
- 🗓️ View interview schedule and timeline
- 📊 Track application status

---

## 🔌 REST API

Base URL: `http://127.0.0.1:8000/api/`

| Endpoint                     | Description               |
|------------------------------|---------------------------|
| `POST /api/auth/token/`      | Get JWT access token      |
| `GET  /api/candidates/`      | List candidates           |
| `GET  /api/job-roles/`       | List job roles            |
| `GET  /api/interviews/`      | List interviews           |
| `GET  /api/feedback/`        | List feedback             |
| `GET  /api/stats/`           | Dashboard analytics       |
| `GET  /api/interviews/upcoming/` | Upcoming interviews   |

Browse the API at: `http://127.0.0.1:8000/api/`

---

## 🛠️ Tech Stack

- **Backend:** Django 4.2, Django REST Framework 3.14
- **Frontend:** Bootstrap 5.3, Chart.js, Bootstrap Icons
- **Auth:** Email-based login, JWT (DRF), Role-based access
- **AI:** Custom resume scoring (skill match + experience ratio)
- **Database:** SQLite (dev) / PostgreSQL-compatible
- **Other:** django-filter, crispy-forms, python-dotenv, Pillow
