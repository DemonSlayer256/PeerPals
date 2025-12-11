from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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
    name = serializers.CharField(max_length=255)
    branch = serializers.CharField(max_length=50, required=False)
    sem = serializers.IntegerField(required=False)
    mid = serializers.CharField(required=False)  # For Student
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
            if not mentor:
                raise serializers.ValidationError(f"Valid mentor ID is required for students. You sent {mentor}")
            mentor_user = User.objects.filter(username = mentor).first()
            if mentor_user is None:
                raise serializers.ValidationError("Mentor does not exist.")
            if not Mentor.objects.filter(user = mentor_user).exists():
                raise serializers.ValidationError("Mentor does not exist.")
        elif role == 'mentor':
            if not data.get('branch'):
                raise serializers.ValidationError('Branch is required for mentors.')
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
                'first_name' : validated_data.pop('name'),
                'email': email,
                'is_staff': is_staff,
                'is_superuser': is_superuser,
                #'password': password,
            }
        )

        if not created:
            # If user exists, raise error
            raise serializers.ValidationError("This User already exists.")

        else:
            # Newly created user, set password
            user.set_password(password)
            user.save()

        # Create or update UserProfile
        UserProfile.objects.create(
            user=user,
            role = role,
        )

        try: # Create related model based on role
            if role == 'student':
                student = Student.objects.create(
                    user=user,
                    branch=validated_data.get('branch'),
                    sem=validated_data.get('sem'),
                    status='Active',
                    mid=Mentor.objects.get(user = User.objects.get(username = validated_data.pop("mid")))
                )
                
                return StudentSerializer(student).data

            elif role == 'mentor':
                mentor = Mentor.objects.create(
                    user=user,
                    branch=validated_data.get('branch'),
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
        fields = ['username', 'email', 'first_name']

# Student serializer
class StudentSerializer(serializers.ModelSerializer):
    usn =serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    mentor_name = serializers.SerializerMethodField()
    name = serializers.CharField(source='user.first_name', read_only=True)
    mid = serializers.CharField(source='mid.user.username', read_only=True)

    class Meta:
        model = Student
        fields = ['name', 'usn', 'branch', 'sem', 'status', 'mentor_name', 'mid',  'email']

        
    def get_mentor_name(self, obj):
        try:
            return obj.mid.user.first_name
        except:
            return None
        
    def get_mid(self, obj):
        try:
            return obj.mid.user.username
        except:
            return None
        
# Mentor serializer
class MentorSerializer(serializers.ModelSerializer):
    mid =serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Mentor
        fields = ['name', 'mid', 'branch', 'contact', 'email']

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
