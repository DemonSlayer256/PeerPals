from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, StudentViewSet, MentorViewSet, FeedbackViewSet, SessionViewSet, LoginAPIView

router = DefaultRouter()
router.register(r'register', RegisterViewSet)
router.register(r'students', StudentViewSet)
router.register(r'mentors', MentorViewSet)
router.register(r'feedbacks', FeedbackViewSet)
router.register(r'sessions', SessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Add login URL
    path('login/', LoginAPIView.as_view(), name='login'),
]