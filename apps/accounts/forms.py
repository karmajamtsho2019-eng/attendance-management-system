from django import forms
from django.core.exceptions import ValidationError

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['college_id', 'first_name', 'last_name', 'email', 'role', 'phone', 'password']

    def clean_college_id(self):
        college_id = (self.cleaned_data.get('college_id') or '').strip()
        if len(college_id) < 3:
            raise ValidationError('College ID must be at least 3 characters long.')
        if User.objects.filter(college_id__iexact=college_id).exists():
            raise ValidationError('A user with this College ID already exists.')
        return college_id

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError('This email address is already registered.')
        return email

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role == User.Role.ADMIN:
            raise ValidationError('Admin accounts must be created through Django admin.')
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.college_id
        user.email = (user.email or '').strip()
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
