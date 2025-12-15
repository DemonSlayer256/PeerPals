from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterViewSet, StudentViewSet, MentorViewSet, FeedbackViewSet, SessionViewSet, LoginAPIView, ChangePasswordAPI

router = DefaultRouter()
router.register(r'register', RegisterViewSet)
router.register(r'students', StudentViewSet)
router.register(r'mentors', MentorViewSet)
router.register(r'feedbacks', FeedbackViewSet)
router.register(r'sessions', SessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Add login URL
    path('change_password/', ChangePasswordAPI.as_view(), name='change_password'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]