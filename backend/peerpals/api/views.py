from rest_framework import viewsets
from .models import Student, Mentor, Feedback, Session
from .serializers import RegistrationSerializer, StudentSerializer, MentorSerializer, FeedbackSerializer, SessionSerializer
from django.contrib.auth.models import User
from rest_framework import permissions


# Create your views here.
def get_user_role(user): 
    if hasattr(user, 'profile'):
        return user.profile.role
    return None

class GetRole(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed = getattr(view, 'allowed_roles', None)
        if allowed is None:
            return False
        role = get_user_role(request.user)
        return role in allowed

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [GetRole]
    allowed_roles = ['admin']
    def perform_create(self, serializer):
        if get_user_role(self.request.user) != 'admin':
            raise permissions.PermissionDenied()
        serializer.save()

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    print("StudentViewSet accessed")
    permission_classes = [permissions.IsAuthenticated, GetRole]
    allowed_roles = ['admin', 'mentor', 'student']
    def perform_create(self, serializer):
        role = get_user_role(self.request.user)
        if role == 'mentor':
            serializer.save()
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
