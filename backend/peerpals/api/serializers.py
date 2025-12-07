from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Student, Mentor, Feedback, Session, UserProfile

class UserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        if 'password_confirm' in self.initial_data:
            if value != self.initial_data['password_confirm']:
                raise serializers.ValidationError("Passwords do not match.")
        validate_password(value)
        return value
    
    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    

class RegistrationSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=['student', 'mentor', 'admin'])
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=50)
    branch = serializers.CharField(max_length=50, required=False)
    sem = serializers.IntegerField(required=False)
    contact = serializers.CharField(max_length=20, required=False)  # For Mentor
    is_staff = serializers.BooleanField(required=False, default=False)  # For Admin

    def validate(self, data):
        role = data.get('role')
        if role == 'student':
            if not data.get('branch') or not data.get('sem'):
                raise serializers.ValidationError("Branch and semester are required for students")
            semester = None
            try:
                semester = int(data.get('sem'))
            except:
                raise serializers.ValidationError("Semesters need to be a number")
            if semester < 1 or semester > 8:
                raise serializers.ValidationError("Semesters should be between 1 - 8")
            mentor = data.get('mid')
            if mentor and not Mentor.objects.filter(id=mentor.id).exists():
                raise serializers.ValidationError("Mentor does not exist.")
        elif role == 'mentor':
            if not data.get('contact'):
                raise serializers.ValidationError("Contact is required for mentors.")
        elif role == 'admin':
            # Additional validation if needed
            pass
        else:
            raise serializers.ValidationError("Invalid role specified.")
        return data
    
    def validate_password(self, value):
        if 'password_confirm' in self.initial_data:
            if value != self.initial_data['password_confirm']:
                raise serializers.ValidationError("Passwords do not match.")
        validate_password(value)
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        is_staff = role == 'admin'
        is_superuser = role == 'admin'

        user = None
        
        # Check if user already exists
        user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': is_staff,
                'is_superuser': is_superuser,
            }
        )

        if not created:
            # If user exists, raise error
            raise serializers.ValidationError("This User already exists.")

        else:
            # Newly created user, set password
            user.set_password(password)

        # Create or update UserProfile
        UserProfile.objects.create(
            user=user,
            role = role,
        )

        try: # Create related model based on role
            if role == 'student':
                student = Student.objects.create(
                    user=user,
                    name=validated_data.get('name'),
                    branch=validated_data.get('branch'),
                    sem=validated_data.get('sem'),
                    status='Active',
                    email=email,
                )
                
                return StudentSerializer(student).data

            elif role == 'mentor':
                mentor = Mentor.objects.create(
                    user=user,
                    name=validated_data.get('name'),
                    branch=validated_data.get('branch', ''),
                    contact=validated_data.get('contact'),
                )
                return MentorSerializer(mentor).data

            elif role == 'admin':
                return UserSerializer(user).data

        except Exception as e:
            # Rollback user creation if necessary
            if user and User.objects.filter(id=user.id).exists():
                user.delete()
            print("Registration error: ", e)
            raise serializers.ValidationError(e)

        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        if not data.get('username') or not data.get('password'):
            raise serializers.ValidationError("Username and password are required.")
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials")
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Student serializer
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_role(self, obj):
        try:
            return obj.user.profile.role
        except UserProfile.DoesNotExist:
            return None
        
# Mentor serializer
class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = Mentor
        fields = '__all__'

    def get_role(self, obj):
        try:
            return obj.user.profile.role
        except UserProfile.DoesNotExist:
            return None

# Feedback serializer
class FeedbackSerializer(serializers.ModelSerializer):
    sid = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), allow_null=True)
    mid = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all())

    class Meta:
        model = Feedback
        fields = '__all__'

    def validate(self, data):
        # Ensure that the student exists and the mentor can give feedback to them
        student = data.get('sid')
        mentor = data.get('mid')

# Session serializer
class SessionSerializer(serializers.ModelSerializer):
    sid = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    mid = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all())

    class Meta:
        model = Session
        fields = '__all__'

    def validate(self, data):
        student = data.get('sid')
        mentor = data.get('mid')

        if student and mentor:
            # Check for conflicting sessions
            existing_sessions = Session.objects.filter(sid=student, mid=mentor, date=data['date'])
            if existing_sessions.exists():
                raise serializers.ValidationError("A session with this student and mentor already exists for this date.")
        else:
            raise serializers.ValidationError("Both student and mentor must be provided.")
        return data
