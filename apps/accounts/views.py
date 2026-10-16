from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.academics.models import Department, Subject
from apps.attendance.models import AttendanceRecord

from .decorators import role_required
from .forms import UserRegistrationForm
from .models import User


def login_view(request):
    if request.method == 'POST':
        college_id = request.POST.get('college_id', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=college_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_redirect')
        return render(request, 'accounts/login.html', {'error': 'Invalid credentials.'})
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard_redirect(request):
    role = request.user.role
    if role == 'ADMIN':
        return redirect('admin_dashboard')
    if role == 'TEACHER':
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')


@login_required
@role_required('ADMIN')
def register_user_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.college_id} created successfully.')
            return redirect('admin_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
@role_required('ADMIN')
def admin_dashboard(request):
    form = UserRegistrationForm()
    if request.method == 'POST' and 'create_user' in request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.college_id} created successfully.')
            return redirect('admin_dashboard')

    users = User.objects.all().order_by('-date_joined')
    departments = Department.objects.all().count()
    subjects = Subject.objects.all().count()
    teachers = User.objects.filter(role='TEACHER').count()
    students = User.objects.filter(role='STUDENT').count()
    recent_attendance = AttendanceRecord.objects.select_related('student', 'subject', 'marked_by').order_by('-date')[:8]
    return render(
        request,
        'accounts/dashboard_admin.html',
        {
            'form': form,
            'total_users': users.count(),
            'teachers': teachers,
            'students': students,
            'departments': departments,
            'subjects': subjects,
            'recent_users': users[:5],
            'recent_attendance': recent_attendance,
        },
    )


@login_required
def teacher_dashboard(request):
    subjects = Subject.objects.count()
    students = User.objects.filter(role='STUDENT').count()
    today_records = AttendanceRecord.objects.filter(marked_by=request.user, date=date.today()).count()
    recent_attendance = AttendanceRecord.objects.filter(marked_by=request.user).select_related('student', 'subject').order_by('-date')[:8]
    return render(
        request,
        'accounts/dashboard_teacher.html',
        {
            'subjects': subjects,
            'students': students,
            'today_records': today_records,
            'recent_attendance': recent_attendance,
        },
    )


@login_required
def student_dashboard(request):
    all_records = request.user.attendance_records.select_related('subject').order_by('-date')
    recent_records = all_records[:10]
    total = all_records.count()
    present = all_records.filter(status='P').count()
    absent = all_records.filter(status='A').count()
    late = all_records.filter(status='L').count()
    present_percentage = round((present / total) * 100, 1) if total else 0
    absent_percentage = round((absent / total) * 100, 1) if total else 0
    late_percentage = round((late / total) * 100, 1) if total else 0
    return render(
        request,
        'accounts/dashboard_student.html',
        {
            'records': recent_records,
            'total': total,
            'present': present,
            'absent': absent,
            'late': late,
            'percentage': present_percentage,
            'present_percentage': present_percentage,
            'absent_percentage': absent_percentage,
            'late_percentage': late_percentage,
        },
    )
