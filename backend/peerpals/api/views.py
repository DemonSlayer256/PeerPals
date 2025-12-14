from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student, Mentor, Feedback, Session
from .serializers import UserPasswordSerializer, RegistrationSerializer, StudentSerializer, MentorSerializer, FeedbackSerializer, SessionSerializer, LoginSerializer
from django.contrib.auth.models import User

# Utility function to get user role
def get_user_role(user): 
    if hasattr(user, 'profile'):
        return user.profile.role
    return None

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return get_user_role(request.user) == 'admin'
    
# Custom Permissions
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == 'admin'

class IsAdminOrMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) in ['admin', 'mentor']

class IsAdminOrStudentOrMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) in ['admin', 'student', 'mentor']

class IsSelf(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own data, or admins to edit any user's data.
    Admins can only set the password during creation.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            # Admins can only set passwords during user creation, not update existing passwords
            if 'password' in request.data:
                return False
            return True

        # Otherwise, users can only edit their own data
        return obj == request.user

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)    
            refresh_token = str(refresh)
            role = get_user_role(user)

            user_data = {}
            if role == 'student':
                student = Student.objects.filter(user=user).first()
                user_data = StudentSerializer(student).data if student else {}
            elif role == 'mentor':
                mentor = Mentor.objects.filter(user=user).first()
                user_data = MentorSerializer(mentor).data if mentor else {}

            return Response({
                'access': access_token,
                'refresh': refresh_token,
                'user_id': user.id,
                'user_data': user_data,
                'username': user.username,
                'role': role,
                'is_staff': user.is_staff
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelf, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'update':
            return UserPasswordSerializer
        return super().get_serializer_class()

    def perform_update(self, serializer):
        user = self.request.user
        if user != self.get_object() and not user.is_staff:
            raise PermissionDenied("You can only update your own password.")
        
        # If the user is an admin, they are only allowed to update the password during user creation
        if user.is_staff and not self.request.data.get('password', None):
            raise PermissionDenied("Admins are not allowed to change passwords after user creation.")
        
        serializer.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # Admins can create users and set their password at the time of creation
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only admins can create users.")

# Register ViewSet
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admins can create users.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()  # currently returns dict
        return Response(result, status=status.HTTP_201_CREATED)


# Student ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStudentOrMentor, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        if get_user_role(self.request.user) == 'admin':
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to add students.")
        
    def perform_update(self, serializer):
        user = self.request.user
        role = get_user_role(user)

        if role == 'student':
            student = Student.objects.get(user=user)
            if student.id != serializer.instance.id:
                raise PermissionDenied("You can only update your own student profile.")
        elif role not in ['admin', 'mentor']:
            raise PermissionDenied("You do not have permission to update student profiles.")
        else:
            serializer.save()

    def get_queryset(self):
        role = get_user_role(self.request.user)

        if role == 'admin':
            return Student.objects.all()
        elif role == 'mentor':
            mentor = Mentor.objects.filter(user=self.request.user).first()
            return Student.objects.filter(mid=mentor) if mentor else Student.objects.none()
        elif role == 'student':
            student = Student.objects.filter(user=self.request.user).first()
            return Student.objects.filter(id=student.id) if student else Student.objects.none()
        return Student.objects.none()

# Mentor ViewSet
class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrMentor, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        if get_user_role(self.request.user) == 'admin':
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to add mentors.")

    def perform_update(self, serializer):
        user = self.request.user
        role = get_user_role(user)

        if role == 'mentor':
            mentor = Mentor.objects.get(user=user)
            if mentor.id != serializer.instance.id:
                raise PermissionDenied("You can only update your own mentor profile.")
        elif role not in ['admin', 'student']:
            raise PermissionDenied("You do not have permission to update mentor profiles.")
        else:
            serializer.save()

# Feedback ViewSet
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStudentOrMentor, IsAdminOrReadOnly]

    # No role restriction, open to all authenticated users

# Session ViewSet
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrMentor, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        role = get_user_role(self.request.user)
        if role in ['admin', 'mentor']:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to add sessions.")
        
    def perform_update(self, serializer):
        role = get_user_role(self.request.user)
        if role in ['admin', 'mentor']:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update sessions.")
