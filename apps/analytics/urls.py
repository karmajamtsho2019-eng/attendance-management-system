from django.urls import path

from . import views

urlpatterns = [
    path('', views.summary_dashboard, name='attendance_summary'),
    path('export-pdf/', views.export_summary_pdf, name='attendance_summary_pdf'),
    path('teacher-breakdown/', views.teacher_breakdown, name='teacher_breakdown'),
    path('student/', views.student_summary, name='student_attendance_summary'),
]
