from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import RefreshToken, TokenObtainPairView
from .models import Student, Mentor, Feedback, Session
from .serializers import RegistrationSerializer, StudentSerializer, MentorSerializer, FeedbackSerializer, SessionSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework import permissions


# Create your views here.
def get_user_role(user): 
    if hasattr(user, 'profile'):
        return user.profile.role
    return None

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
                try:
                    student = Student.objects.get(user=user)
                    user_data = StudentSerializer(student).data
                except Student.DoesNotExist:
                    user_data = {}
            elif role == 'mentor':
                try:
                    mentor = Mentor.objects.get(user=user)
                    user_data = MentorSerializer(mentor).data
                except Mentor.DoesNotExist:
                    user_data = {}
            

            return Response({
                'access': access_token,
                'refresh': refresh_token,
                'user_id': user.id,
                'user_data': user_data,
                'username': user.username,
                'role': get_user_role(user),
            }, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class IsAuthenticatedAndRole(permissions.BasePermission):
    allowed_roles = []
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = get_user_role(request.user)
        return role in self.allowed_roles
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == 'admin'
    
class IsAdminOrMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        role = get_user_role(request.user)
        return role == 'mentor'
    
class IsAdminOrStudentOrMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        role = get_user_role(request.user)
        return role in ['admin', 'student', 'mentor']
    

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAdmin]
    def perform_create(self, serializer):
        serializer.save()

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    print("StudentViewSet accessed")
    permission_classes = [permissions.IsAuthenticated, IsAdminOrMentorOrStudent]
    def perform_create(self, serializer):
        serializer.save()
    def get_queryset(self):
        role = get_user_role(self.request.user)
        if role == 'admin':
            return Student.objects.all()
        elif role == 'mentor':
            try:
                mentor = Mentor.objects.get(user=self.request.user)
                return Student.objects.filter(roll_no__gte=mentor.start_roll_no, roll_no__lte=mentor.end_roll_no)
            except Mentor.DoesNotExist:
                return Student.objects.none()
        else:
            try:
                student = Student.objects.get(user=self.request.user)
                return Student.objects.filter(id=student.id)
            except Student.DoesNotExist:
                return Student.objects.none()
        return Student.objects.none()

class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStudentOrMentor]
    def perform_create(self, serializer):
        role = get_user_role(self.request.user)
        if role in ['admin']:
            serializer.save()
        else:
            raise permissions.PermissionDenied()
    
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStudentOrMentor]

    # def update(self, request, *args, **kwargs):
    #     feedback = self.get_object()
    #     user = request.user
    #     role = get_user_role(user)
    #     if role 
    # No role restriction, open to all authenticated users

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrMentor]
    def perform_create(self, serializer):
        user = self.request.user
        role = get_user_role(user)
        if role in ['admin', 'mentor']:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to add sessions.")
        
    def perform_update(self, serializer):
        user = self.request.user
        role = get_user_role(user)
        if role not in ['mentor', 'admin']:
            raise PermissionDenied("You do not have permission to update sessions")
        serializer.save()