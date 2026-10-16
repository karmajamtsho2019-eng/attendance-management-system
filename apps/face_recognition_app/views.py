from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import role_required
from apps.attendance.models import AttendanceRecord

from .models import AIAttendanceSession
from .services import EnrollmentError, enroll_face_image, recognize_classroom_photo


@login_required
def enroll_face_view(request):
    if request.method == 'POST':
        angle_label = request.POST.get('angle_label', 'front')
        image_file = request.FILES.get('photo')
        try:
            enroll_face_image(request.user, image_file, angle_label)
            return render(request, 'face_recognition/enroll.html', {'success': True})
        except EnrollmentError as exc:
            return render(request, 'face_recognition/enroll.html', {'error': str(exc)})
    return render(request, 'face_recognition/enroll.html')


@login_required
@role_required('TEACHER')
def upload_classroom_photo_view(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        date = request.POST.get('date')
        session_number = request.POST.get('session_number', 1)
        photo = request.FILES.get('photo')
        if not photo or not subject_id or not date:
            return render(request, 'face_recognition/upload.html', {'error': 'Subject, date and photo are required.'})

        session = AIAttendanceSession.objects.create(
            subject_id=subject_id,
            teacher=request.user,
            classroom_photo=photo,
            date=date,
            session_number=session_number,
        )
        results = recognize_classroom_photo(session.classroom_photo.path)
        session.detected_faces_count = len(results)
        session.save()

        request.session['pending_results'] = [
            {
                'student_id': result['student'].id if result['student'] else None,
                'student_name': result['student'].get_full_name() if result['student'] else 'Unknown',
                'confidence': result['confidence'],
                'status': result['status'],
            }
            for result in results
        ]
        request.session['ai_session_id'] = session.id
        return redirect('review_ai_attendance')

    return render(request, 'face_recognition/upload.html')


@login_required
@role_required('TEACHER')
def review_ai_attendance_view(request):
    results = request.session.get('pending_results', [])
    if request.method == 'POST':
        ai_session_id = request.session.get('ai_session_id')
        ai_session = get_object_or_404(AIAttendanceSession, id=ai_session_id)
        saved = 0
        for key, value in request.POST.items():
            if key.startswith('confirm_') and value == 'present':
                student_id = key.replace('confirm_', '')
                AttendanceRecord.objects.get_or_create(
                    student_id=student_id,
                    subject=ai_session.subject,
                    date=ai_session.date,
                    session=ai_session.session_number,
                    defaults={
                        'marked_by': request.user,
                        'status': 'P',
                        'source': AttendanceRecord.Source.FACE,
                        'confidence': None,
                    },
                )
                saved += 1
        ai_session.status = AIAttendanceSession.SessionStatus.CONFIRMED
        ai_session.save()
        request.session.pop('pending_results', None)
        request.session.pop('ai_session_id', None)
        return render(request, 'face_recognition/confirmed.html', {'saved': saved})
    return render(request, 'face_recognition/review.html', {'results': results})
