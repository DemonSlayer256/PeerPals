from rest_framework import viewsets
from .models import Student, Mentor, Feedback, Session
from .serializers import StudentSerializer, MentorSerializer, FeedbackSerializer, SessionSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


# Create your views here.
def get_user_role(user): 
    if hasattr(user, 'profile'):
        return user.profile.role
    return None

class GetRole(BasePermission):
    def has_permission(self, request, view):
        allowed = getattr(view, 'allowed_roles', None)
        if allowed is None:
            return False
        role = get_user_role(request.user)
        return role in allowed_roles

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, GetRole]
    allowed_roles = ['admin', 'mentor', 'student']

    def perform_create(self, serializer):
        role = get_user_role(self.request.user)
        if role == 'student':
            serializer.save(user=self.request.user)
        elif role == 'admin':
            serializer.save()
        else:
            raise permissions.PermissionDenied()

class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticated, GetRole]
    allowed_roles = ['admin', 'mentor']

    def perform_create(self, serializer):
        role = get_user_role(self.request.user)
        if role in ['admin', 'mentor']:
            serializer.save()
        else:
            raise permissions.PermissionDenied()

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    # No role restriction, open to all authenticated users

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]
