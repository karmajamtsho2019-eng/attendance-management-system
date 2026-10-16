from django.db import models

from apps.accounts.models import User


class FaceImage(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='face_images')
    image = models.ImageField(upload_to='face_data/raw/%Y/%m/')
    angle_label = models.CharField(max_length=20)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.college_id} - {self.angle_label}'


class FaceEmbedding(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='embeddings')
    source_image = models.ForeignKey(FaceImage, on_delete=models.CASCADE)
    vector = models.JSONField()
    model_version = models.CharField(max_length=20, default='v1')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.college_id} embedding ({self.model_version})'


class AIAttendanceSession(models.Model):
    class SessionStatus(models.TextChoices):
        PENDING_REVIEW = 'PENDING', 'Pending Teacher Review'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    subject = models.ForeignKey('academics.Subject', on_delete=models.PROTECT)
    teacher = models.ForeignKey(User, on_delete=models.PROTECT)
    classroom_photo = models.ImageField(upload_to='face_data/sessions/%Y/%m/')
    date = models.DateField()
    session_number = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=10, choices=SessionStatus.choices, default=SessionStatus.PENDING_REVIEW)
    detected_faces_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject.code} - {self.date} - {self.status}'
