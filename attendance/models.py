from django.db import models
from datetime import date
from django.utils import timezone


class Student(models.Model):
    name = models.CharField(max_length=100, null=True)
    roll_number = models.CharField(max_length=10, null=True)
    student_class = models.CharField(max_length=10, null=True)
    section = models.CharField(max_length=5, null=True)

    def __str__(self):
        return f'{self.name} ({self.roll_number}){self.student_class}{self.section}'


class Myclass(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('od', 'On Duty')
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.id:  # If the instance is being created (not updating)
            self.date = date.today()  # Set the date field to the current date
        super().save(*args, **kwargs)  # Call the parent class's save method


