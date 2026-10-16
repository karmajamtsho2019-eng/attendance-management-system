from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.attendance.api_views import AttendanceRecordViewSet

router = DefaultRouter()
router.register(r'attendance', AttendanceRecordViewSet, basename='attendance')


def root_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    return redirect('login')


urlpatterns = [
    path('', root_view),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('face/', include('apps.face_recognition_app.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
