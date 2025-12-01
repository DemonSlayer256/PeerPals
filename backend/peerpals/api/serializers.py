from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Mentor, Feedback, Session, UserProfile

# User serializer for basic user info

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True)   

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, data):
        if data['password'] < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return data
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(**validated_data)
        if role == 'student':
            UserProfile.objects.create(user=user, role='student')
        elif role == 'mentor': 
            UserProfile.objects.create(user=user, role='mentor')
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Student serializer
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Student
        fields = '__all__'

# Mentor serializer
class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Mentor
        fields = '__all__'

# Feedback serializer
class FeedbackSerializer(serializers.ModelSerializer):
    sid = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), allow_null=True)
    mid = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all())

    class Meta:
        model = Feedback
        fields = '__all__'

# Session serializer
class SessionSerializer(serializers.ModelSerializer):
    sid = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    mid = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all())

    class Meta:
        model = Session
        fields = '__all__'