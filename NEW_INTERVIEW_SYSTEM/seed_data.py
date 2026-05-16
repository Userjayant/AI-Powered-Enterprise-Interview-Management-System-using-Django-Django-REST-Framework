"""
seed_data.py
Run: python seed_data.py
Creates demo users, job roles, candidates, interviews, and feedback.
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from candidates.models import JobRole, Candidate
from interviews.models import Interview, Feedback
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


def create_demo_users():
    print("Creating demo users...")

    # HR Admin
    hr, _ = User.objects.get_or_create(email='hr@demo.com', defaults={
        'username': 'hr_admin',
        'first_name': 'Priya',
        'last_name': 'Sharma',
        'role': 'hr_admin',
        'department': 'hr',
        'phone_number': '9876543210',
        'is_verified': True,
        'is_staff': True,
    })
    hr.set_password('demo1234')
    hr.save()

    # Interviewer 1
    iv1, _ = User.objects.get_or_create(email='interviewer@demo.com', defaults={
        'username': 'senior_dev',
        'first_name': 'Arjun',
        'last_name': 'Mehta',
        'role': 'interviewer',
        'department': 'engineering',
        'phone_number': '9988776655',
        'is_verified': True,
    })
    iv1.set_password('demo1234')
    iv1.save()

    # Interviewer 2
    iv2, _ = User.objects.get_or_create(email='tech_lead@demo.com', defaults={
        'username': 'tech_lead',
        'first_name': 'Kavya',
        'last_name': 'Reddy',
        'role': 'interviewer',
        'department': 'engineering',
        'is_verified': True,
    })
    iv2.set_password('demo1234')
    iv2.save()

    # Candidate User
    cu, _ = User.objects.get_or_create(email='candidate@demo.com', defaults={
        'username': 'demo_candidate',
        'first_name': 'Rahul',
        'last_name': 'Gupta',
        'role': 'candidate',
        'is_verified': True,
    })
    cu.set_password('demo1234')
    cu.save()

    # Superuser
    if not User.objects.filter(is_superuser=True).exists():
        su = User.objects.create_superuser(
            username='admin',
            email='admin@demo.com',
            password='admin1234',
            first_name='Super',
            last_name='Admin',
            role='hr_admin',
        )
        print(f"  Superuser: admin@demo.com / admin1234")

    print(f"  HR Admin:   hr@demo.com / demo1234")
    print(f"  Interviewer: interviewer@demo.com / demo1234")
    print(f"  Candidate:  candidate@demo.com / demo1234")
    return hr, iv1, iv2, cu


def create_job_roles(hr):
    print("Creating job roles...")
    roles_data = [
        {
            'title': 'Senior Python Developer',
            'department': 'Engineering',
            'required_skills': 'Python, Django, REST API, PostgreSQL, Redis, Docker',
            'job_description': 'We are looking for an experienced Python developer to join our backend team. You will design and implement high-performance APIs and microservices.',
            'minimum_experience': 3,
        },
        {
            'title': 'React Frontend Engineer',
            'department': 'Engineering',
            'required_skills': 'React, JavaScript, TypeScript, HTML, CSS, Redux, Webpack',
            'job_description': 'Join our frontend team to build beautiful, responsive user interfaces for our SaaS platform used by thousands of businesses.',
            'minimum_experience': 2,
        },
        {
            'title': 'DevOps Engineer',
            'department': 'Operations',
            'required_skills': 'AWS, Docker, Kubernetes, CI/CD, Terraform, Linux, Jenkins',
            'job_description': 'We need a skilled DevOps engineer to manage our cloud infrastructure and deployment pipelines.',
            'minimum_experience': 3,
        },
        {
            'title': 'Product Manager',
            'department': 'Product',
            'required_skills': 'Product Strategy, Agile, Jira, User Research, Data Analysis, Roadmapping',
            'job_description': 'Drive product vision and strategy for our core platform. Work closely with engineering, design, and customers.',
            'minimum_experience': 4,
        },
        {
            'title': 'Data Science Engineer',
            'department': 'Engineering',
            'required_skills': 'Python, Machine Learning, TensorFlow, SQL, Pandas, NumPy, scikit-learn',
            'job_description': 'Build ML models and data pipelines to power our AI-driven recommendation engine.',
            'minimum_experience': 2,
        },
        {
            'title': 'UI/UX Designer',
            'department': 'Design',
            'required_skills': 'Figma, UI Design, UX Research, Prototyping, Adobe XD, Design Systems',
            'job_description': 'Create beautiful and intuitive designs for our web and mobile applications.',
            'minimum_experience': 2,
        },
    ]
    roles = []
    for data in roles_data:
        role, _ = JobRole.objects.get_or_create(title=data['title'], defaults={**data, 'created_by': hr})
        roles.append(role)
    print(f"  Created {len(roles)} job roles.")
    return roles


def create_candidates(roles, candidate_user):
    print("Creating candidates...")
    candidates_data = [
        {
            'full_name': 'Rahul Gupta',
            'email': 'candidate@demo.com',
            'phone': '9876543211',
            'skills': 'Python, Django, REST API, PostgreSQL, Redis',
            'experience': 4.0,
            'current_company': 'TechCorp India',
            'current_ctc': 12.0,
            'expected_ctc': 18.0,
            'notice_period': 30,
            'linkedin_profile': 'https://linkedin.com/in/rahulgupta',
            'github_profile': 'https://github.com/rahulgupta',
            'source': 'LinkedIn',
            'status': 'shortlisted',
            'role_idx': 0,
            'user': candidate_user,
        },
        {
            'full_name': 'Sneha Patel',
            'email': 'sneha.patel@email.com',
            'phone': '9876543212',
            'skills': 'React, JavaScript, TypeScript, Redux, CSS, HTML',
            'experience': 3.5,
            'current_company': 'WebSolutions Ltd',
            'current_ctc': 10.0,
            'expected_ctc': 15.0,
            'notice_period': 45,
            'linkedin_profile': 'https://linkedin.com/in/snehapatel',
            'source': 'Referral',
            'status': 'interview_scheduled',
            'role_idx': 1,
        },
        {
            'full_name': 'Kiran Nair',
            'email': 'kiran.nair@email.com',
            'phone': '9876543213',
            'skills': 'AWS, Docker, Kubernetes, CI/CD, Linux, Terraform',
            'experience': 5.0,
            'current_company': 'CloudBase Systems',
            'current_ctc': 18.0,
            'expected_ctc': 25.0,
            'notice_period': 60,
            'source': 'Job Portal',
            'status': 'selected',
            'role_idx': 2,
        },
        {
            'full_name': 'Ananya Singh',
            'email': 'ananya.singh@email.com',
            'phone': '9876543214',
            'skills': 'Python, Machine Learning, TensorFlow, SQL, Pandas, scikit-learn',
            'experience': 2.5,
            'current_company': 'DataMinds',
            'current_ctc': 9.0,
            'expected_ctc': 14.0,
            'notice_period': 30,
            'github_profile': 'https://github.com/ananyasingh',
            'source': 'Campus Recruitment',
            'status': 'applied',
            'role_idx': 4,
        },
        {
            'full_name': 'Mohammed Faiz',
            'email': 'faiz.ahmed@email.com',
            'phone': '9876543215',
            'skills': 'Python, Django, PostgreSQL, Docker',
            'experience': 2.0,
            'current_company': 'StartupX',
            'current_ctc': 7.0,
            'expected_ctc': 11.0,
            'notice_period': 15,
            'source': 'LinkedIn',
            'status': 'rejected',
            'role_idx': 0,
        },
        {
            'full_name': 'Preethi Rajan',
            'email': 'preethi.rajan@email.com',
            'phone': '9876543216',
            'skills': 'Figma, UI Design, UX Research, Prototyping, Adobe XD',
            'experience': 3.0,
            'current_company': 'DesignStudio',
            'current_ctc': 8.0,
            'expected_ctc': 13.0,
            'notice_period': 30,
            'linkedin_profile': 'https://linkedin.com/in/preethirajan',
            'source': 'Portfolio',
            'status': 'interview_completed',
            'role_idx': 5,
        },
        {
            'full_name': 'Vikram Joshi',
            'email': 'vikram.joshi@email.com',
            'phone': '9876543217',
            'skills': 'Product Strategy, Agile, Jira, User Research, Data Analysis',
            'experience': 5.5,
            'current_company': 'ProductFirst',
            'current_ctc': 20.0,
            'expected_ctc': 28.0,
            'notice_period': 90,
            'source': 'Referral',
            'status': 'on_hold',
            'role_idx': 3,
        },
        {
            'full_name': 'Divya Krishnan',
            'email': 'divya.krishnan@email.com',
            'phone': '9876543218',
            'skills': 'React, TypeScript, GraphQL, Node.js, CSS',
            'experience': 1.5,
            'current_company': 'Fresher',
            'current_ctc': 0,
            'expected_ctc': 7.0,
            'notice_period': 0,
            'source': 'Campus',
            'status': 'screening',
            'role_idx': 1,
        },
    ]

    candidates = []
    for data in candidates_data:
        role_idx = data.pop('role_idx')
        user = data.pop('user', None)
        role = roles[role_idx] if role_idx < len(roles) else None
        c, created = Candidate.objects.get_or_create(email=data['email'], defaults={
            **data,
            'applied_role': role,
            'user': user,
        })
        if created:
            c.ai_resume_score = c.compute_ai_score()
            c.save()
        candidates.append(c)

    print(f"  Created {len(candidates)} candidates.")
    return candidates


def create_interviews(candidates, interviewers, hr):
    print("Creating interviews...")
    iv1, iv2 = interviewers
    now = timezone.now()

    interviews_data = [
        {
            'candidate_idx': 0,
            'interviewer': iv1,
            'round_type': 'technical_1',
            'scheduled_at': now + timedelta(days=2, hours=10),
            'duration': 60,
            'mode': 'online',
            'meeting_link': 'https://meet.google.com/abc-defg-hij',
            'status': 'scheduled',
            'notes': 'Focus on Django REST Framework and database design.',
        },
        {
            'candidate_idx': 1,
            'interviewer': iv2,
            'round_type': 'screening',
            'scheduled_at': now + timedelta(days=1, hours=11),
            'duration': 30,
            'mode': 'phone',
            'status': 'scheduled',
        },
        {
            'candidate_idx': 2,
            'interviewer': iv1,
            'round_type': 'technical_1',
            'scheduled_at': now - timedelta(days=5),
            'duration': 90,
            'mode': 'online',
            'meeting_link': 'https://meet.google.com/xyz-uvwx-ijk',
            'status': 'completed',
        },
        {
            'candidate_idx': 2,
            'interviewer': hr,
            'round_type': 'hr_final',
            'scheduled_at': now - timedelta(days=2),
            'duration': 45,
            'mode': 'online',
            'status': 'completed',
        },
        {
            'candidate_idx': 5,
            'interviewer': iv2,
            'round_type': 'technical_1',
            'scheduled_at': now - timedelta(days=3),
            'duration': 60,
            'mode': 'in_person',
            'location': 'Conference Room B, Floor 3',
            'status': 'completed',
        },
        {
            'candidate_idx': 0,
            'interviewer': hr,
            'round_type': 'screening',
            'scheduled_at': now - timedelta(days=7),
            'duration': 30,
            'mode': 'phone',
            'status': 'completed',
        },
        {
            'candidate_idx': 3,
            'interviewer': iv1,
            'round_type': 'technical_1',
            'scheduled_at': now + timedelta(days=4, hours=14),
            'duration': 90,
            'mode': 'online',
            'meeting_link': 'https://meet.google.com/ml-interview-link',
            'status': 'scheduled',
        },
    ]

    created_interviews = []
    for data in interviews_data:
        cidx = data.pop('candidate_idx')
        if cidx >= len(candidates):
            continue
        iview, _ = Interview.objects.get_or_create(
            candidate=candidates[cidx],
            round_type=data['round_type'],
            defaults={**data, 'scheduled_by': hr}
        )
        created_interviews.append(iview)

    print(f"  Created {len(created_interviews)} interviews.")
    return created_interviews


def create_feedback(interviews, interviewers):
    print("Creating feedback...")
    iv1, iv2 = interviewers

    completed = [i for i in interviews if i.status == 'completed']
    feedback_data_list = [
        {'technical': 8.5, 'communication': 7.0, 'problem_solving': 8.0, 'confidence': 7.5, 'recommendation': 'hire',
         'strengths': 'Strong system design skills, excellent knowledge of distributed systems.',
         'weaknesses': 'Could improve on frontend understanding.',
         'comments': 'Very strong candidate overall, demonstrated deep backend expertise.',
         'interviewer': iv1},
        {'technical': 9.0, 'communication': 8.5, 'problem_solving': 9.0, 'confidence': 8.0, 'recommendation': 'strong_hire',
         'strengths': 'Exceptional communication, culture fit is excellent.',
         'weaknesses': 'Minor gaps in negotiation tactics.',
         'comments': 'Best candidate we have interviewed this quarter. Highly recommend.',
         'interviewer': iv1},
        {'technical': 6.5, 'communication': 7.5, 'problem_solving': 6.0, 'confidence': 7.0, 'recommendation': 'maybe',
         'strengths': 'Creative thinking, good design portfolio.',
         'weaknesses': 'Needs more experience with enterprise design systems.',
         'comments': 'Good candidate but may need 6 more months of experience.',
         'interviewer': iv2},
        {'technical': 7.0, 'communication': 8.0, 'problem_solving': 7.5, 'confidence': 8.5, 'recommendation': 'hire',
         'strengths': 'Excellent communication, great attitude, fast learner.',
         'weaknesses': 'Limited experience with large-scale systems.',
         'comments': 'Would be a great addition to the team with proper mentorship.',
         'interviewer': iv1},
    ]

    count = 0
    for i, interview in enumerate(completed[:len(feedback_data_list)]):
        if not interview.has_feedback():
            fd = feedback_data_list[i]
            Feedback.objects.create(
                interview=interview,
                submitted_by=fd['interviewer'],
                technical_score=fd['technical'],
                communication_score=fd['communication'],
                problem_solving_score=fd['problem_solving'],
                confidence_score=fd['confidence'],
                strengths=fd['strengths'],
                weaknesses=fd['weaknesses'],
                comments=fd['comments'],
                recommendation=fd['recommendation'],
            )
            count += 1

    print(f"  Created {count} feedback records.")


def main():
    print("\n" + "="*50)
    print("  InterviewIQ — Seeding Demo Data")
    print("="*50 + "\n")

    hr, iv1, iv2, cu = create_demo_users()
    roles = create_job_roles(hr)
    candidates = create_candidates(roles, cu)
    interviews = create_interviews(candidates, [iv1, iv2], hr)
    create_feedback(interviews, [iv1, iv2])

    print("\n" + "="*50)
    print("  ✅ Demo data created successfully!")
    print("="*50)
    print("\n🚀 Run: python manage.py runserver")
    print("🌐 Open: http://127.0.0.1:8000\n")


if __name__ == '__main__':
    main()
