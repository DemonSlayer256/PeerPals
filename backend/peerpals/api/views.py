from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from .models import Student, Mentor, Feedback, Session
from .serializers import UserPasswordSerializer, RegistrationSerializer, StudentSerializer, MentorSerializer, FeedbackSerializer, SessionSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.core.signing import dumps, BadSignature, SignatureExpired, loads

User = get_user_model()

#Utility function for generation of verification tokens
def token_gen(user):
    username = None
    for i in ['usn', 'mid']:
        if i in user:
            username = user[i]
            break
    payload = {"username" : username, "verified" : user['is_verified']}
    return dumps(payload, salt = 'email-verification')

def verify_email_token(token, max_age=3600):
    try:
        data = loads(token, salt="email-verification", max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None

    username = data.get("username")
    verified_at_issue = data.get("verified")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    # Invalidate tokens issued before verification
    if user.is_verified != verified_at_issue:
        return None

    return user


#Utility function for sending verification mails
def send_verif_mail(user, request):
    token = token_gen(user)
    verification_link = f"{request.scheme}://{request.get_host()}{reverse('verify_email', args=[token])}"
    send_mail(
        subject="Welcome to PeerPals 👋 Let's verify your email",
        message=(
            "Hey there! 👋\n\n"
            "Welcome to PeerPals — we're excited to have you on board!\n\n"
            "Before you get started, please take a quick moment to verify your email "
            "by clicking the link below:\n\n"
            f"{verification_link}\n\n"
            "This helps us keep your account secure and makes sure you don't miss "
            "any important updates.\n\n"
            "If you didn't sign up for PeerPals, you can safely ignore this email.\n\n"
            "See you inside!\n"
            "— The PeerPals Team 🚀"
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user["email"]],
        fail_silently=False,
    )

# Utility function to get user role
def get_user_role(user): 
    if hasattr(user, 'profile'):
        return user.profile.role
    return None

class IsEmailVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'is_verified', False)
    
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return get_user_role(request.user) == 'admin'
        return True
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
    Admins can only set the password during creation in future but for now they can edit. 
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            # Admins can only set passwords during user creation, not update existing passwords
            if 'password' in request.data:
                return False
            return True

        # Otherwise, users can only edit their own data
        return obj == request.user

class VerifyEmailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        user = verify_email_token(token)

        if not user:
            return Response(
                {"detail": "Verification link is invalid or expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_verified = True
        user.save(update_fields=["is_verified"])

        return Response(
            {"detail": "Email verified successfully!"},
            status=status.HTTP_200_OK
        )

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny, IsAdminOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)    
            refresh_token = str(refresh)
            role = get_user_role(user)
            requested_role = request.data.get('requested_role')
            if role != requested_role:
                error_message = f"Login restricted: Please sign in as a {role.capitalize()}."
                return Response({'detail': error_message}, status=status.HTTP_401_UNAUTHORIZED)

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
                'user_data': user_data,
                'username': user.username,
                'first_name': user.first_name, # <-- ADD THIS LINE
                'last_name': user.last_name,
                'role': role,
                'is_staff': user.is_staff
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User ViewSet
class ChangePasswordAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        user_req = self.request.user
        uid = user_req.id
        user = User.objects.get(id=uid)
        if user.is_staff:
            raise PermissionDenied("You can only update your own password.")
        serializer = UserPasswordSerializer(data=request.data, context={'user': user})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# Register ViewSet
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            result = serializer.save()
            send_verif_mail(result, request)
            return Response(result, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateMixin:
    """
    Adds bulk + single PATCH support to a ModelViewSet.
    Assumes the serializer supports partial updates and each item has an 'id'.
    """

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        user = request.user
        role = get_user_role(user)
        
        if role in ['student', 'mentor']:
            raise PermissionDenied("Only admin can update details")
        data = request.data

        # Bulk update
        if isinstance(data, list):
            ids = [item.get('id') for item in data if 'id' in item]

            if not ids:
                return Response(
                    {"detail": "Each item must include an 'id'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            instances = self.get_queryset().filter(id__in=ids)

            if instances.count() != len(ids):
                existing_ids = set(instances.values_list('id', flat=True))
                missing_ids = set(ids) - existing_ids
                return Response(
                    {"detail": f"Invalid IDs: {list(missing_ids)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            instance_map = {inst.id: inst for inst in instances}
            updated_results = []

            for item in data:
                instance = instance_map[item['id']]
                serializer = self.get_serializer(instance, data=item, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_results.append(serializer.data)

            return Response(updated_results, status=status.HTTP_200_OK)

        # Single update (detail route)
        return self.partial_update(request, *args, **kwargs)

# Student ViewSet
class StudentViewSet(viewsets.ModelViewSet, UpdateMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStudentOrMentor, IsEmailVerified]

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
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Mentor ViewSet
class MentorViewSet(viewsets.ModelViewSet, UpdateMixin):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmailVerified]

    def get_queryset(self):
        role = get_user_role(self.request.user)

        if role == 'admin':
            return Mentor.objects.all()
        elif role == 'mentor':
            mentor = Mentor.objects.filter(user=self.request.user).first()
            return Mentor.objects.filter(id=mentor.id) if mentor else Mentor.objects.none()
        elif role == 'student':
            student = Student.objects.filter(user=self.request.user).first()
            if student and student.mid:
                return Mentor.objects.filter(branch=student.branch)
        return Mentor.objects.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Feedback ViewSet
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly, IsEmailVerified]

    # No role restriction, open to all authenticated users
    def create(self, serializer):
        role = get_user_role(self.request.user)
        if role in ['admin', 'mentor']:
            raise PermissionDenied("Only students can give feedback")
        sent_data = self.request.data.copy()
        student = Student.objects.get(user=self.request.user)
        sent_data['sid'] = student.id
        sent_data['mid'] = student.mid.id
        serializer = self.get_serializer(data=sent_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  

    def get_queryset(self):
        user_role = get_user_role(self.request.user)
        if user_role == 'mentor':
            return self.queryset.filter(mid=Mentor.objects.get(user = self.request.user))
        elif user_role == 'student':
            return self.queryset.filter(sid=Student.objects.get(user = self.request.user))
        elif user_role == 'admin':
            return self.queryset.all()
        return self.queryset.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

# Session ViewSet
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmailVerified]

    def create(self, request, *args, **kwargs):
        if get_user_role(self.request.user) == 'student':
            # Student will only send description, title and anon
            sent_data = self.request.data.copy()
            student = Student.objects.get(user=self.request.user)
            sent_data['sid'] = student.id
            sent_data['status'] = 'request'
            sent_data['mid'] = student.mid.id
            serializer = self.get_serializer(data=sent_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        else:
            raise PermissionDenied("Only students can create session requests.")
        
    def perform_update(self, serializer):
        if get_user_role(self.request.user) != 'mentor':
            raise PermissionDenied("Only mentors can update session details")
        status = serializer.validated_data.get('status', serializer.instance.status)
        if status == 'request':
            raise ValidationError("Mentors cannot change status back to 'request'")
        serializer.save()


    def get_queryset(self):
        user_role = get_user_role(self.request.user)
        if user_role == 'mentor':
            return self.queryset.filter(mid=Mentor.objects.get(user = self.request.user))
        elif user_role == 'student':
            return self.queryset.filter(sid=Student.objects.get(user = self.request.user))
        elif user_role == 'admin':
            return self.queryset.all()
        return self.queryset.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)