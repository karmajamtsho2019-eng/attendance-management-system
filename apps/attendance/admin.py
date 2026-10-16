from django.contrib import admin

from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'session', 'status', 'source', 'marked_by')
    list_filter = ('status', 'source', 'date', 'subject')
    search_fields = ('student__college_id', 'subject__code', 'marked_by__college_id')
