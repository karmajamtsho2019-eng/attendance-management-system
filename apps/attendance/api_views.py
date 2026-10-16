from rest_framework import permissions, viewsets

from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            return AttendanceRecord.objects.filter(student=user)
        if user.role == 'TEACHER':
            return AttendanceRecord.objects.filter(marked_by=user)
        return AttendanceRecord.objects.all()
