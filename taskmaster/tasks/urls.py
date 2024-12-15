from django.urls import path
from .views import RegisterView, LoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # User Mangagement endpoints
    path('users/register/', RegisterView.as_view(), name='register_user'),
    path('users/login/', LoginView.as_view(), name='login_user'),
    path('users/logout/', LogoutView.as_view(), name='logout_user'),
     # Endpoint to obtain authentication token
    path('users/token/', obtain_auth_token, name='obtain_auth_token'),
]