import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render

from apps.accounts.decorators import role_required
from apps.accounts.models import User
from .forms import AttendanceExportForm, AttendanceSessionForm
from .models import AttendanceRecord


@login_required
@role_required('TEACHER', 'ADMIN')
def mark_attendance_view(request):
    if request.method == 'POST' and 'load_students' in request.POST:
        form = AttendanceSessionForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            class_name = form.cleaned_data.get('class_name') or f'{subject.code} - {subject.name}'
            students = User.objects.filter(role='STUDENT').order_by('college_id')
            return render(
                request,
                'attendance/mark.html',
                {
                    'form': form,
                    'students': students,
                    'subject_id': subject.id,
                    'subject': subject,
                    'class_name': class_name,
                    'date': form.cleaned_data['date'],
                    'session': form.cleaned_data['session'],
                },
            )
    if request.method == 'POST' and 'save_attendance' in request.POST:
        subject_id = request.POST.get('subject_id')
        date = request.POST.get('date')
        session = request.POST.get('session')
        saved = 0
        skipped = 0
        for key, value in request.POST.items():
            if key.startswith('status_'):
                student_id = key.replace('status_', '')
                try:
                    AttendanceRecord.objects.create(
                        student_id=student_id,
                        subject_id=subject_id,
                        marked_by=request.user,
                        date=date,
                        session=session,
                        status=value,
                        source=AttendanceRecord.Source.MANUAL,
                    )
                    saved += 1
                except IntegrityError:
                    skipped += 1
        messages.success(request, f'Attendance saved for {saved} students.')
        return render(request, 'attendance/success.html', {'saved': saved, 'skipped': skipped})

    form = AttendanceSessionForm()
    return render(request, 'attendance/select_class.html', {'form': form})


@login_required
@role_required('TEACHER', 'ADMIN')
def export_attendance_view(request):
    form = AttendanceExportForm(request.POST or None)
    records = []

    if request.method == 'POST' and form.is_valid():
        subject = form.cleaned_data['subject']
        target_date = form.cleaned_data['date']
        records = AttendanceRecord.objects.filter(subject=subject, date=target_date).select_related('student', 'subject', 'marked_by').order_by('student__college_id')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="attendance-{subject.code}-{target_date}.csv"'
        writer = csv.writer(response)
        writer.writerow(['College ID', 'Student Name', 'Subject', 'Date', 'Session', 'Status', 'Marked By'])
        for item in records:
            writer.writerow([
                item.student.college_id,
                item.student.get_full_name() or '-',
                item.subject.code,
                item.date,
                item.session,
                item.get_status_display(),
                item.marked_by.college_id,
            ])
        return response

    return render(request, 'attendance/export.html', {'form': form, 'records': records})
