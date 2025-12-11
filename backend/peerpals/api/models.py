from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=50)
    sem = models.IntegerField()
    status = models.CharField(max_length=20)
    mid = models.ForeignKey('Mentor', on_delete=models.SET_NULL, null=True, blank=True, default=None)  

    def __str__(self):
        return f"{self.user.first_name}"

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.first_name}"

class Feedback(models.Model):
    sid = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL)
    mid = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Session(models.Model):
    sid = models.ForeignKey(Student, on_delete=models.CASCADE)
    mid = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)  # scheduled / completed

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('mentor', 'Mentor'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} - {self.get_role_display()}"