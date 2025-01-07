from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    # User Mangagement endpoints
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    # Endpoint to obtain authentication token
    path('token/', obtain_auth_token, name='obtain_auth_token'),
    # router to automatically generate appropriate url patterns for the crud operations
    path('', include(router.urls)),
]