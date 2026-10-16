from collections import defaultdict
from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.accounts.models import User
from apps.attendance.models import AttendanceRecord


def _get_date_range(request):
    start_date = request.GET.get('start_date') or request.POST.get('start_date')
    end_date = request.GET.get('end_date') or request.POST.get('end_date')
    if start_date:
        start_date = date.fromisoformat(start_date)
    if end_date:
        end_date = date.fromisoformat(end_date)
    return start_date, end_date


def _filter_records_by_date(records, start_date=None, end_date=None):
    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)
    return records


def _build_subject_summary(records):
    subject_summary = defaultdict(lambda: {'total': 0, 'present': 0, 'absent': 0, 'late': 0})
    for record in records:
        bucket = subject_summary[record.subject.code]
        bucket['total'] += 1
        if record.status == 'P':
            bucket['present'] += 1
        elif record.status == 'A':
            bucket['absent'] += 1
        elif record.status == 'L':
            bucket['late'] += 1
    subject_rows = []
    for subject_code, values in sorted(subject_summary.items()):
        total_for_subject = values['total']
        present_count = values['present']
        subject_rows.append({
            'subject_code': subject_code,
            'total': total_for_subject,
            'present': present_count,
            'absent': values['absent'],
            'late': values['late'],
            'percentage': round((present_count / total_for_subject) * 100, 1) if total_for_subject else 0,
        })
    return subject_rows


@login_required
def summary_dashboard(request):
    if request.user.role == 'STUDENT':
        return student_summary(request)

    start_date, end_date = _get_date_range(request)
    records = AttendanceRecord.objects.select_related('student', 'subject', 'marked_by').order_by('-date', 'subject__code')
    records = _filter_records_by_date(records, start_date, end_date)

    total = records.count()
    present = records.filter(status='P').count()
    absent = records.filter(status='A').count()
    late = records.filter(status='L').count()
    subject_rows = _build_subject_summary(records)
    overall_percentage = round((present / total) * 100, 1) if total else 0
    absent_percentage = round((absent / total) * 100, 1) if total else 0
    late_percentage = round((late / total) * 100, 1) if total else 0

    return render(
        request,
        'analytics/summary.html',
        {
            'records': records[:12],
            'total': total,
            'present': present,
            'absent': absent,
            'late': late,
            'subject_rows': subject_rows,
            'overall_percentage': overall_percentage,
            'absent_percentage': absent_percentage,
            'late_percentage': late_percentage,
            'start_date': start_date,
            'end_date': end_date,
        },
    )


@login_required
def export_summary_pdf(request):
    start_date, end_date = _get_date_range(request)
    records = AttendanceRecord.objects.select_related('student', 'subject', 'marked_by').order_by('-date', 'subject__code')
    records = _filter_records_by_date(records, start_date, end_date)

    total = records.count()
    present = records.filter(status='P').count()
    absent = records.filter(status='A').count()
    late = records.filter(status='L').count()
    subject_rows = _build_subject_summary(records)

    response = HttpResponse(content_type='application/pdf')
    filename = 'attendance-summary.pdf'
    if start_date or end_date:
        filename = f'attendance-summary-{start_date or "start"}-to-{end_date or "end"}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    styles = getSampleStyleSheet()
    story = [Paragraph('Attendance Summary Report', styles['Title'])]
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            f'Period: {start_date or "All time"} to {end_date or "Latest"}',
            styles['BodyText'],
        )
    )
    story.append(Spacer(1, 12))

    summary_table = Table(
        [
            ['Total Records', str(total)],
            ['Present', str(present)],
            ['Absent', str(absent)],
            ['Late', str(late)],
            ['Present %', f'{round((present / total) * 100, 1) if total else 0}%'],
        ],
        colWidths=[220, 120],
    )
    summary_table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ])
    )
    story.append(summary_table)
    story.append(Spacer(1, 18))

    subject_data = [['Subject', 'Present', 'Absent', 'Late', 'Presence %']]
    for row in subject_rows:
        subject_data.append([
            row['subject_code'],
            str(row['present']),
            str(row['absent']),
            str(row['late']),
            f"{row['percentage']}%",
        ])
    subject_table = Table(subject_data, colWidths=[120, 80, 80, 80, 90])
    subject_table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dfeaf7')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ])
    )
    story.append(subject_table)

    doc = SimpleDocTemplate(response, pagesize=letter)
    doc.build(story)
    return response


@login_required
def teacher_breakdown(request):
    if request.user.role not in {'TEACHER', 'ADMIN'}:
        raise PermissionDenied('This report is only available to teachers and admins.')

    start_date, end_date = _get_date_range(request)
    records = AttendanceRecord.objects.select_related('student', 'subject', 'marked_by').order_by('-date', 'subject__code')
    if request.user.role == 'TEACHER':
        records = records.filter(marked_by=request.user)
    records = _filter_records_by_date(records, start_date, end_date)

    breakdown_rows = []
    for record in records:
        breakdown_rows.append({
            'date': record.date,
            'subject': record.subject.code,
            'student': record.student.college_id,
            'status': record.get_status_display(),
            'session': record.session,
            'marked_by': record.marked_by.college_id,
        })

    return render(
        request,
        'analytics/teacher_breakdown.html',
        {
            'records': breakdown_rows,
            'start_date': start_date,
            'end_date': end_date,
            'total': len(breakdown_rows),
        },
    )


@login_required
def student_summary(request):
    records = request.user.attendance_records.select_related('subject').order_by('-date')
    total = records.count()
    present = records.filter(status='P').count()
    absent = records.filter(status='A').count()
    late = records.filter(status='L').count()

    subject_rows = _build_subject_summary(records)
    overall_percentage = round((present / total) * 100, 1) if total else 0
    absent_percentage = round((absent / total) * 100, 1) if total else 0
    late_percentage = round((late / total) * 100, 1) if total else 0

    return render(
        request,
        'analytics/student_summary.html',
        {
            'records': records[:10],
            'subject_rows': subject_rows,
            'total': total,
            'present': present,
            'absent': absent,
            'late': late,
            'overall_percentage': overall_percentage,
            'present_percentage': overall_percentage,
            'absent_percentage': absent_percentage,
            'late_percentage': late_percentage,
        },
    )
