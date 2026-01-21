from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    is_verified = models.BooleanField(default = False)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    branch = models.CharField(max_length=50)
    sem = models.IntegerField()
    status = models.CharField(max_length=20)
    mid = models.ForeignKey('Mentor', on_delete=models.SET_NULL, null=True, blank=True, default=None)  
    max_sessions = models.IntegerField(default=5)

    def session_this_month(self):
        from django.utils.timezone import now
        today = now().date()
        first_day = today.replace(day=1)
        return Session.objects.filter(
            sid=self,
            date__gte=first_day,
            date__month=today.month,
            date__year=today.year
        ).count()
    
    def can_create_session(self):
        return self.session_this_month() < self.max_sessions
    
    def __str__(self):
        return f"{self.user.username}"

class Mentor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    branch = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}"

class Feedback(models.Model):
    sid = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL)
    mid = models.ForeignKey(Mentor, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    anon = models.BooleanField(null = True)

class Session(models.Model):
    STATUS_CHOICES = (
        ('accept', "Accepted"),
        ('request', "Requested"),
        ('completed', "Completed"),
    )
    sid = models.ForeignKey(Student, on_delete=models.CASCADE)
    mid = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    date = models.DateField(null = True)
    title = models.TextField(blank = False, null = False, default = "Null")
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices = STATUS_CHOICES)  # scheduled / completed
    anon =  models.BooleanField(default=False)

    def __call__(self, *args, **kwds):
        return f"Session on {self.date} between {self.sid.user.first_name} and {self.mid.user.first_name}"
    
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('mentor', 'Mentor'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} - {self.get_role_display()}"