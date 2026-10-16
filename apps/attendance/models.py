from django.db import models

from apps.accounts.models import User
from apps.academics.models import Subject


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'P', 'Present'
        ABSENT = 'A', 'Absent'
        LATE = 'L', 'Late'

    class Source(models.TextChoices):
        MANUAL = 'MANUAL', 'Manual Entry'
        FACE = 'FACE_RECOGNITION', 'AI Face Recognition'

    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    marked_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='marked_attendance')
    date = models.DateField()
    session = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=1, choices=Status.choices)
    source = models.CharField(max_length=20, choices=Source.choices)
    confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject', 'date', 'session'],
                name='one_record_per_student_per_session',
            )
        ]
        indexes = [
            models.Index(fields=['date', 'subject']),
            models.Index(fields=['student', 'date']),
        ]

    def __str__(self):
        return f'{self.student.college_id} - {self.subject.code} - {self.date} - {self.status}'
