from django.urls import path

from . import views

urlpatterns = [
    path('mark/', views.mark_attendance_view, name='mark_attendance'),
    path('export/', views.export_attendance_view, name='export_attendance'),
]
