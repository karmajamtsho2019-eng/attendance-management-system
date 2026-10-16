# Attendance Management System

A Django-based attendance management system with role-based access, attendance analytics, CSV export, and AI-assisted facial attendance using uploaded classroom images.

## Features
- Admin, teacher, and student dashboards
- Custom college ID login
- Manual attendance marking
- Attendance summaries and subject-wise reporting
- CSV export for attendance records
- AI face recognition workflow using uploaded student and classroom images
- Sidebar-based modern dashboard UI

## Tech Stack
- Python 3.12
- Django 5
- PostgreSQL-ready configuration
- SQLite for local development
- Django REST Framework
- face_recognition / dlib

## Project Structure
- `apps/accounts` - authentication and role-based users
- `apps/academics` - departments and subjects
- `apps/attendance` - attendance records and manual attendance flow
- `apps/analytics` - reporting and summary pages
- `apps/face_recognition_app` - face recognition enrollment and matching workflow
- `templates/` - dashboard and UI templates

## Local Setup
1. Open a terminal in the project folder.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser or use the demo credentials already set up in the app.
6. Start the app:
   ```bash
   python manage.py runserver
   ```

## Demo Accounts
- Admin: `admin-demo` / `admin123`
- Teacher: `teacher-demo` / `teacher123`
- Student: `student-demo` / `student123`

## Notes
This project is suitable as a capstone/demo application for attendance management and AI-assisted attendance workflows. The face-recognition feature is designed around uploaded images and can be extended for live camera-based capture in future versions.
