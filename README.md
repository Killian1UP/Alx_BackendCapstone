# Alx_BackendCapstone

Installed and configured rest_framework.authtoken:
Added 'rest_framework.authtoken' to my INSTALLED_APPS in settings.py.

Ran migrations to create the necessary database tables for token management:
python manage.py migrate

Authenticate Users in Views: Used token-based authentication for user-related views by including 'rest_framework.authentication.TokenAuthentication' in my DEFAULT_AUTHENTICATION_CLASSES.

in urls.py i add a url for thr authentication:
path('users/token/', obtain_auth_token, name='obtain_auth_token'),

How It Works:
Endpoint: POST /users/token/
Purpose: Allows a user to obtain an authentication token after providing valid credentials (username and password).
Request Payload:
{
    "username": "yourusername",
    "password": "yourpassword"
}

Response Example:
{
    "token": "a9f84a74e5f889b13a2392c123456789abcdef1234"
}