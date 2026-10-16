from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('college_id', 'role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Info', {'fields': ('college_id', 'role', 'phone')}),
    )
    list_display = ('college_id', 'email', 'role', 'is_staff')
    search_fields = ('college_id', 'email', 'first_name', 'last_name')
