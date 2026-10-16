from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, college_id=None, email=None, password=None, **extra_fields):
        if not college_id:
            raise ValueError('The college_id field must be set.')

        extra_fields.setdefault('username', college_id)
        email = self.normalize_email(email)
        user = self.model(college_id=college_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, college_id=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(college_id=college_id, email=email, password=password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'

    college_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=Role.choices)
    phone = models.CharField(max_length=15, blank=True, default='')

    USERNAME_FIELD = 'college_id'
    REQUIRED_FIELDS = ['email', 'role']
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.college_id} ({self.get_role_display()})'
