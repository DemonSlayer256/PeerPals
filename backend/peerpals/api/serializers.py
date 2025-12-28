from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Student, Mentor, Feedback, Session, UserProfile
from datetime import date, timedelta, datetime

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
    
class RoleValidationMixin:
    def validate_sem(self, value):
        try:
            semester = int(value)
        except:
            raise serializers.ValidationError("Semesters need to be a number")
        if semester < 1 or semester > 8:
            raise serializers.ValidationError("Semesters should be between 1 - 8")
        return semester

    def validate_mid(self, mentor):
        if not mentor:
            raise serializers.ValidationError(f"Valid mentor ID is required for students. You sent {mentor}")
        mentor_user = User.objects.filter(username = mentor).first()
        if mentor_user is None:
            raise serializers.ValidationError("Mentor does not exist.")
        obj = Mentor.objects.filter(user = mentor_user).first()
        if not obj:
            raise serializers.ValidationError("Mentor does not exist.")
        return obj
            
    def validate_branch(self, value):
        if not value:
            raise serializers.ValidationError('Branch is required.')
        return value
    
    def validate_contact(self, value):
        if not value:
            raise serializers.ValidationError("Contact is required for mentors.")
        return value
        
class RegistrationSerializer(serializers.Serializer, RoleValidationMixin):
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
            self.validate_sem(data.get('sem', None))
            self.validate_branch(data.get('branch', None))
            self.validate_mid(data.get('mid', None))

        elif role == 'mentor':
            self.validate_branch(data.get('branch', None))
            self.validate_contact(data.get('contact', None))

        else:
            self.validate_contact(data.get('contact', None))

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
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name' : validated_data.pop('name'),
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
                    mid=validated_data.pop("mid"),
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
class StudentSerializer(serializers.ModelSerializer, RoleValidationMixin):
    usn = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    name = serializers.CharField(source='user.first_name')
    mid = serializers.CharField(required=False)  # Allow 'mid' to be updated in a PATCH request

    class Meta:
        model = Student
        fields = ['name', 'usn', 'branch', 'sem', 'status', 'mid', 'email']

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
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['mentor_name'] = self.get_mentor_name(instance)
        representation['mid'] = self.get_mid(instance)
        representation['id'] = instance.id
        return representation

    def update(self, instance, validated_data):
        """ Perform the update for the Student model """
        # Update the user-related fields
        try:
            user = validated_data.pop('user')
            # Update other fields normally
            for attr, value in user.items():
                setattr(instance.user, attr, value)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

        except Exception as e:
            raise serializers.ValidationError(str(e))
        return instance

# Mentor serializer
class MentorSerializer(serializers.ModelSerializer, RoleValidationMixin):
    mid =serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    name = serializers.CharField(source='user.first_name')

    class Meta:
        model = Mentor
        fields = ['name', 'mid', 'branch', 'contact', 'email']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = instance.id
        return rep
    
    def update(self, instance, validated_data):
        """ Perform the update for the Mentor model """
        # Update the user-related fields
        try:
            if "user" in validated_data:
                user = validated_data.pop('user')
                # Update other fields normally
                for attr, value in user.items():
                    setattr(instance.user, attr, value)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

        except Exception as e:
            raise serializers.ValidationError(str(e))

        return instance
    
    
# Feedback serializer
class FeedbackSerializer(serializers.ModelSerializer):
    sid = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True)
    mid = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all())
    text = serializers.CharField(max_length=500, allow_null=True)
    date = serializers.DateField()
    rating = serializers.IntegerField(min_value = 1, max_value = 5, allow_null=True)
    anon = serializers.BooleanField(write_only=True)

    class Meta:
        model = Feedback
        fields = ['sid', 'mid', 'text', 'date', 'rating', 'anon']


    def to_representation(self, instance):
        # This method customizes the representation of the instance
        representation = super().to_representation(instance)

        representation['student'] = "Anonymous" if instance.anon else instance.sid.user.first_name if instance.sid else None
        representation['usn'] = "Anonymous" if instance.anon else instance.sid.user.username if instance.sid else None
        representation['mentor_name'] = instance.mid.user.first_name if instance.mid else None
        representation['mid'] = instance.mid.user.username

        return representation

    def validate(self, data):
        student = data.get('sid')
        mentor = data.get('mid')
        session_date = data.get('date')  # Corrected to use 'date' as it is in the fields

        if not all([student, mentor]):
            raise serializers.ValidationError("Both student and mentor must be provided")

        if not Session.objects.filter(sid=student, mid=mentor, date=session_date).exists():
            raise serializers.ValidationError("Cannot give feedback on a non-existent session.")
        
        if Feedback.objects.filter(sid = student, mid = mentor, date = session_date).exists():
            raise serializers.ValidationError("Already provided feedback")
        
        return data


# Session serializer
class SessionSerializer(serializers.Serializer):
    sid = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True)
    mid = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all(), write_only=True)
    date = serializers.DateField(required=False)
    title = serializers.CharField(max_length = 100, required = False)
    description = serializers.CharField(allow_blank=True, required=False)
    status = serializers.ChoiceField(choices = ['accept', 'request','completed'])
    anon = serializers.BooleanField(write_only=True)
    student = serializers.SerializerMethodField()
    mentor_name = serializers.SerializerMethodField()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['mid'] = self.get_mid(instance)
        rep['usn'] = self.get_usn(instance)
        rep['id'] = instance.id
        return rep
    
    def get_usn(self, obj):
        try:
            if obj.anon:
                return "Anonymous"
            return obj.sid.user.username
        except:
            return None
        
    def get_mentor_name(self, obj):
        try:
            return obj.mid.user.first_name
        except:
            return None
        
    def get_student(self, obj):
        try:
            if obj.anon:
                return "Anonymous"
            return obj.sid.user.first_name
        except:
            return None
        
    def get_mid(self, obj):
        try:
            return obj.mid.user.username
        except:
            return None
        
    class Meta:
        model = Session
        fields = ['id', 'title', 'student', 'mentor_name', 'date', 'description', 'status']

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        student = attrs.get('sid') or getattr(instance, 'sid', None)
        mentor = attrs.get('mid') or getattr(instance, 'mid', None)
        session_date = attrs.get('date')

        # Normalize session_date to a date object if datetime
        if isinstance(session_date, datetime):
            session_date = session_date.date()

        status = self.validate_status(attrs.get('status')) 
        if status == 'request' and not attrs.get('title', None):
            raise serializers.ValidationError("Title cannot be empty. Please enter a value")
        
        if instance:
            if session_date and status == 'accept':
                limit_date = date.today() + timedelta(days=30)
                if session_date > limit_date:
                    raise serializers.ValidationError(
                        "The session date cannot be more than one month from today."
                    )
                if session_date < date.today():
                    raise serializers.ValidationError("Sessions cannot be set in the past")
            else:
                raise serializers.ValidationError("Cannot accept a session without setting a date.")
            return attrs

        if student.mid != mentor:
            raise serializers.ValidationError(
                "This student is not assigned to the specified mentor."
            )

        # Monthly session limit check
        if not student.can_create_session():
            raise serializers.ValidationError(
                f"Student has reached the maximum of {student.max_sessions} sessions this month."
            )

        # Duplicate session check for the date
        existing_sessions = Session.objects.filter(
            sid=student,
            mid=mentor,
            date=session_date
        )

        if existing_sessions.exists():
            if existing_sessions.filter(status__in=['accept', 'completed']).exists():
                raise serializers.ValidationError(
                    "A session with this student and mentor already exists for this date."
                )
            else:
                raise serializers.ValidationError(
                    "A session request has already been made with this mentor."
                )

        return attrs

    def validate_status(self, new_status):

        instance = getattr(self, 'instance', None)

        # POST
        if not instance:
            if new_status != 'request':
                raise serializers.ValidationError(
                    "New sessions must start with status 'request'."
                )
            return new_status

        # PATCH
        current_status = instance.status

        # Terminal state
        if current_status == 'completed':
            raise serializers.ValidationError(
                "Completed sessions cannot be modified."
            )

        allowed_transitions = {
            'request': ['accept'],
            'accept': ['completed'],
        }

        if new_status != current_status:
            if new_status not in allowed_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Invalid status transition: {current_status} → {new_status}"
                )
                
        return new_status

    
    def create(self, validated_data):
        # Use the passed Student and Mentor objects directly
        sid = validated_data.pop('sid')
        mid = validated_data.pop('mid')
        description = validated_data.get('description')
        title = validated_data.pop('title')

        
        # Create the session, assuming you have a 'Session' model
        session = Session.objects.create(sid=sid, mid=mid, title = title,description=description, status=validated_data.get('status'), anon=validated_data.get('anon'))
        return session
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance