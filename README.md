# Smart Attendance System

A Django-based attendance management system designed for colleges and educational institutions. The project supports role-based access, manual attendance recording, analytics dashboards, and AI-assisted attendance using face recognition from uploaded images.

## Project Overview
The Smart Attendance System solves common classroom challenges such as time-consuming manual attendance, duplicate marking, and limited visibility into student participation. Teachers can mark attendance quickly, admins can manage user accounts, and students can review their attendance history through a modern dashboard interface.

## Key Features
- Role-based authentication for admin, teacher, and student users
- College ID login flow built on a custom Django user model
- Manual attendance marking by subject, date, and session
- Attendance summary dashboard with subject-wise stats
- Present, absent, and late tracking
- CSV export for attendance reports
- AI face-recognition workflow using uploaded student and classroom images
- Modern responsive UI with sidebar navigation

## Tech Stack
- Python 3.12
- Django 5
- SQLite for local development
- PostgreSQL-ready configuration
- Django REST Framework
- NumPy
- face_recognition / dlib
- HTML, CSS, and Django templates

## Application Modules
- `apps/accounts` — login, registration, role access, and dashboard logic
- `apps/academics` — departments and subjects
- `apps/attendance` — attendance records and manual attendance flow
- `apps/analytics` — attendance summaries, filters, and reports
- `apps/face_recognition_app` — face enrollment and classroom recognition flow
- `templates/` — dashboard and UI front-end templates

## Demo Credentials
- Admin: `admin-demo` / `admin123`
- Teacher: `teacher-demo` / `teacher123`
- Student: `student-demo` / `student123`

## Local Setup
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the app:
   ```bash
   python manage.py runserver
   ```
6. Open the app in your browser at:
   ```bash
   http://127.0.0.1:8000/
   ```

## Future Enhancements
- Real-time webcam attendance capture
- Better face-recognition thresholds and model tuning
- Advanced student analytics and downloadable PDF reports
- Multi-classroom and multi-department reporting
- Deployment to cloud platforms such as Render or Railway

## Project Status
This project is suitable for a final-year academic demo, portfolio showcase, and capstone presentation. It demonstrates a complete full-stack workflow for attendance management with AI support and data reporting.
