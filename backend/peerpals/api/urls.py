from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, MentorViewSet, FeedbackViewSet, SessionViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'mentors', MentorViewSet)
router.register(r'feedbacks', FeedbackViewSet)
router.register(r'sessions', SessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]