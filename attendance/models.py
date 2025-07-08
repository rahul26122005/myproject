from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=True)  # Changed null=True to blank=True
    roll_number = models.CharField(max_length=100, blank=True, unique=True)  # Unique constraint added
    student_class = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=80, blank=True)
    
    def __str__(self):
        return f'{self.name} ({self.roll_number}){self.student_class}{self.section}{self.user}'

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent'), ('od', 'OD')])

    class Meta:
        unique_together = ('student', 'date', 'status')
