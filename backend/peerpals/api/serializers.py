from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Mentor, Feedback, Session, UserProfile

# User serializer for basic user info
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