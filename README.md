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

Project Idea: Taskmaster - A Task Management API

Overview - 

Taskmaster is a task management API built with Django and Django Rest Framework (DRF). The application allows users to create, update, and manage tasks efficiently. Additionally, it includes user authentication, registration, and token-based authentication for secure access. Taskmaster is designed to provide a seamless experience for managing personal and work-related tasks.

Key Features -

User Authentication & Registration: Users can register, log in, and authenticate via token-based authentication.

Task Management: Users can create, update, delete, and retrieve tasks, ensuring effective task tracking.

User Roles: Each user has personalized access to their tasks, ensuring data privacy and security.

Logging: The application includes error logging for debugging and system monitoring purposes.

Technologies that will be used - 

Python 3.x: Programming language for the backend.

Django: Web framework for building the API.

Django Rest Framework (DRF): Used for building the API endpoints and handling user authentication.

MySQL: Relational database used for storing user data and tasks.

JWT Token Authentication: For secure, token-based user authentication.

Git: Version control for managing code changes.