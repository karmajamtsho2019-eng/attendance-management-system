from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    department = models.ForeignKey('Department', on_delete=models.PROTECT, related_name='subjects')
    semester = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('code', 'semester')

    def __str__(self):
        return f'{self.code} - {self.name}'
