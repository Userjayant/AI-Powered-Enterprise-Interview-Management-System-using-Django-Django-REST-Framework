<div align="center">

# 🚀 AI-Powered Enterprise Interview Management System  
### using Django & Django REST Framework

<p align="center">

<img src="https://img.shields.io/badge/Django-6.0-green?style=for-the-badge&logo=django" />
<img src="https://img.shields.io/badge/Django_REST_Framework-DRF-red?style=for-the-badge&logo=django" />
<img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap" />
<img src="https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite" />
<img src="https://img.shields.io/badge/Status-Under_Development-orange?style=for-the-badge" />

</p>

---

### 🏢 Enterprise-Level HR Recruitment & Interview Management Platform

A modern enterprise-grade recruitment platform built using **Django** and **Django REST Framework** that simulates real-world company hiring workflows including candidate management, interview scheduling, technical evaluations, AI resume screening, analytics dashboards, and role-based authentication.

---

</div>

# 📌 Features

## 🔐 Authentication & Role Management
- Custom User Model
- Role-Based Access Control
- HR / Interviewer / Candidate Dashboards
- Login / Logout System
- Profile Management
- Password Reset

---

## 👨‍💼 Candidate Management
- Add / Edit / Delete Candidates
- Resume Upload System
- Skills & Experience Tracking
- Candidate Status Tracking
- Candidate Profiles

---

## 📅 Interview Management
- Interview Scheduling
- Multiple Interview Rounds
- Assign Interviewers
- Technical / HR / Final Rounds
- Interview Status Tracking

---

## 🧠 AI Resume Screening
- Resume Keyword Matching
- Skill Extraction
- AI Resume Score Generation
- Candidate Ranking

---

## 📝 Feedback & Evaluation
- Technical Evaluation
- Communication Evaluation
- Problem Solving Assessment
- Interviewer Recommendations
- Final Hiring Decisions

---

## 📊 Analytics Dashboard
- Total Candidates
- Selected Candidates
- Interview Statistics
- Hiring Analytics
- Dashboard Cards & Charts

---

## 🌐 REST API Development
- DRF Serializers
- API Endpoints
- Token Authentication
- Role-Based APIs
- JSON Responses

---

# 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python 3.12 | Backend Development |
| Django | Web Framework |
| Django REST Framework | API Development |
| Bootstrap 5 | Frontend UI |
| SQLite | Development Database |
| HTML5 / CSS3 / JS | Frontend Design |
| Pillow | Image Uploads |
| Django Filters | Search & Filtering |

---

# 📂 Project Structure

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

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Userjayant/AI-Powered-Enterprise-Interview-Management-System-using-Django-Django-REST-Framework.git
```

---

## Navigate to Project

```bash
cd AI-Powered-Enterprise-Interview-Management-System-using-Django-Django-REST-Framework
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

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Run Development Server

```bash
python manage.py runserver
```

---

# 🚀 Future Enhancements

- AI-Based Resume Parsing
- Email Notification System
- Real-Time Interview Tracking
- Calendar Integration
- Advanced Analytics Dashboard
- PostgreSQL Deployment
- Docker Deployment
- JWT Authentication
- Live Interview Monitoring

---

# 👨‍💻 Developer

### Jayant Thevarakonda

Final Year B.Tech AI Student  
Web Developer | Django Developer | AI Enthusiast

---

# ⭐ Project Status

🚧 Currently Under Professional Development

---

# 📜 License

This project is developed for educational, portfolio, and internship assessment purposes.

```
