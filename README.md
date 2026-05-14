<div align="center">

<img src="https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/DRF-3.14-ff1709?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>

# 💼 AI-Powered Enterprise Interview Management System using Django & Django REST Framework

**A production-quality, enterprise-grade recruitment platform built with Django & Django REST Framework.**  
Streamline your entire hiring pipeline — from job posting to final selection — with AI resume scoring, role-based dashboards, and real-time analytics.

[Features](#-features) • [Tech Stack](#-tech-stack) • [Setup](#-local-setup) • [API](#-rest-api) • [Screenshots](#-project-structure) • [Demo](#-demo-credentials)

</div>

---

## 📌 Project Overview

**InterviewIQ** is a full-stack Interview Management System designed to simulate real-world enterprise HR software. It supports three distinct user roles — HR Admin, Interviewer, and Candidate — each with their own dashboard, permissions, and workflow.

The system features an **AI Resume Scoring Engine** that automatically evaluates candidates based on skill match percentage and experience weighting against job requirements, providing instant hiring signals to HR teams.

---

## ✨ Features

### 👩‍💼 HR Admin
- 📊 Analytics Dashboard — pipeline charts, monthly trends, department breakdown (Chart.js)
- 👥 Full Candidate Management — add, edit, filter, update pipeline status
- 💼 Job Role Management — create and manage open positions with skill requirements
- 📅 Interview Scheduling — assign interviewers, set date/time/mode, auto email notifications
- 🤖 AI Resume Scoring — automatic skill keyword matching + experience ratio scoring (0–100%)
- 🔍 Advanced Search & Filter — by status, role, skills, date
- 👷 Staff Management — create Interviewer and HR Admin accounts
- 🔌 REST API Explorer — full DRF browsable API

### 🎯 Interviewer
- 📋 Personal dashboard — today's interviews, upcoming schedule
- ✅ Structured Feedback Submission — 4-dimension scoring (Technical, Communication, Problem Solving, Confidence)
- 📈 Performance tracking — average scores given, pending feedback count
- 🔒 Access control — only sees own assigned interviews

### 🙋 Candidate
- 📝 Self-registration and profile management
- 📄 Resume upload and application submission
- 🗓️ Interview timeline with real-time status tracking
- 📊 Application progress from Applied → Shortlisted → Selected

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | Django 4.2 |
| **REST API** | Django REST Framework 3.14 |
| **Authentication** | Email-based login, JWT (SimpleJWT), Session Auth |
| **Frontend** | Bootstrap 5.3, Chart.js, Bootstrap Icons |
| **Database** | SQLite (dev) / PostgreSQL-compatible |
| **File Handling** | Pillow (image), FileField (resume) |
| **Forms** | django-crispy-forms + crispy-bootstrap5 |
| **Filtering** | django-filter |
| **Config** | python-dotenv |
| **CORS** | django-cors-headers |

---

## 📁 Project Structure

AI-Powered Enterprise Interview Management System
│
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
├── .env
│
├── logs/
├── media/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── vendor/
│
├── templates/
│   ├── base.html
│   ├── navbar.html
│   ├── sidebar.html
│   ├── messages.html
│   └── components/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── migrations/
│   ├── templates/accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── change_password.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   ├── views.py
│   └── utils.py
│
├── candidates/
│   ├── migrations/
│   ├── templates/candidates/
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── create.html
│   │   ├── update.html
│   │   ├── delete.html
│   │   ├── job_list.html
│   │   └── job_form.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── filters.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── interviews/
│   ├── migrations/
│   ├── templates/interviews/
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── schedule.html
│   │   ├── edit.html
│   │   ├── calendar.html
│   │   ├── feedback_form.html
│   │   └── feedback_detail.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── dashboard/
│   ├── templates/dashboard/
│   │   ├── hr_dashboard.html
│   │   ├── interviewer_dashboard.html
│   │   ├── candidate_dashboard.html
│   │   └── analytics.html
│   │
│   ├── __init__.py
│   ├── urls.py
│   └── views.py
│
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── permissions.py
│   └── pagination.py
│
└── venv/

## ⚙️ Local Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/interviewiq.git
cd interviewiq

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment file
cp .env.example .env
# Open .env and set a strong SECRET_KEY

# 5. Create required directories
mkdir -p logs static media

# 6. Apply database migrations
python manage.py makemigrations accounts candidates interviews
python manage.py migrate

# 7. Seed demo data
python seed_data.py

# 8. Run the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000**

---

## 🔐 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| 🔴 HR Admin | `hr@demo.com` | `demo1234` |
| 🟡 Interviewer | `interviewer@demo.com` | `demo1234` |
| 🟢 Candidate | `candidate@demo.com` | `demo1234` |
| ⚫ Django Admin | `admin@demo.com` | `admin1234` |

> Django Admin panel: **http://127.0.0.1:8000/admin/**

---

## 🔌 REST API

Base URL: `http://127.0.0.1:8000/api/`

### Authentication
```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "hr@demo.com",
  "password": "demo1234"
}
```

### Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/api/auth/token/` | Obtain JWT token | Public |
| `POST` | `/api/auth/token/refresh/` | Refresh JWT token | Public |
| `GET` | `/api/candidates/` | List all candidates | HR Admin |
| `POST` | `/api/candidates/` | Create candidate | HR Admin |
| `GET` | `/api/candidates/{id}/` | Candidate detail | HR Admin |
| `POST` | `/api/candidates/{id}/compute_score/` | Recompute AI score | HR Admin |
| `POST` | `/api/candidates/{id}/update_status/` | Update pipeline status | HR Admin |
| `GET` | `/api/job-roles/` | List job roles | All |
| `GET` | `/api/job-roles/{id}/candidates/` | Candidates for a role | HR Admin |
| `GET` | `/api/interviews/` | List interviews | Role-filtered |
| `GET` | `/api/interviews/upcoming/` | Upcoming interviews | Role-filtered |
| `GET` | `/api/interviews/today/` | Today's interviews | Role-filtered |
| `GET` | `/api/feedback/` | List feedback | Role-filtered |
| `GET` | `/api/stats/` | Dashboard analytics | HR Admin |

> Browse the full API at: **http://127.0.0.1:8000/api/**

---

## 🤖 AI Resume Scoring Logic

The scoring engine runs automatically when a candidate is added or updated:
Score = Skill Match (60%) + Experience Match (25%) + Profile Completeness (15%)
Skill Match    → (Matched Skills / Required Skills) × 60
Experience     → min(candidate_exp / required_exp, 1.5) × 25
Completeness   → +5 for LinkedIn, +5 for GitHub, +5 for Resume upload
Final Score    → 0 to 100%
---

## 🗃️ Database Models
User          → Custom user model with role (hr_admin / interviewer / candidate)
JobRole       → Open positions with required skills and description
Candidate     → Full profile, resume, CTC, AI score, pipeline status
Interview     → Scheduling with round type, mode, meeting link, status
Feedback      → 4-dimension scoring, strengths, weaknesses, recommendation
---

## 🔒 Role-Based Access

| Feature | HR Admin | Interviewer | Candidate |
|---------|----------|-------------|-----------|
| View all candidates | ✅ | ❌ | ❌ |
| Add / edit candidates | ✅ | ❌ | ❌ |
| Schedule interviews | ✅ | ❌ | ❌ |
| Submit feedback | ✅ | ✅ (own only) | ❌ |
| View own interviews | ✅ | ✅ | ✅ |
| Manage staff accounts | ✅ | ❌ | ❌ |
| Access analytics | ✅ | ❌ | ❌ |
| Update own application | ❌ | ❌ | ✅ |

---

## 👨‍💻 Author

Jayant TN
📧 jayanttn0407@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/jayant-tn-72759b243/)  
🐙 [GitHub](https://github.com/Userjayant)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with ❤️ using Django · DRF · Bootstrap 5</sub>
</div>
