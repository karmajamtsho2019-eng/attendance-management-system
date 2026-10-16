from django.urls import path

from . import views

urlpatterns = [
    path('enroll/', views.enroll_face_view, name='enroll_face'),
    path('upload/', views.upload_classroom_photo_view, name='upload_classroom_photo'),
    path('review/', views.review_ai_attendance_view, name='review_ai_attendance'),
]
