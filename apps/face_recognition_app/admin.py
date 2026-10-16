from django.contrib import admin

from .models import AIAttendanceSession, FaceEmbedding, FaceImage


@admin.register(FaceImage)
class FaceImageAdmin(admin.ModelAdmin):
    list_display = ('student', 'angle_label', 'uploaded_at')
    search_fields = ('student__college_id',)


@admin.register(FaceEmbedding)
class FaceEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('student', 'model_version', 'is_active', 'created_at')
    list_filter = ('is_active', 'model_version')
    search_fields = ('student__college_id',)


@admin.register(AIAttendanceSession)
class AIAttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'date', 'session_number', 'status', 'detected_faces_count')
    list_filter = ('status', 'date')
