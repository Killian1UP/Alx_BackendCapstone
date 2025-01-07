from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User

User = get_user_model()  # Dynamically fetch the custom user model

# Endpoint for registering a new user
class RegisterView(APIView):
    permission_classes = [AllowAny]  
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)  # Deserialize incoming user data
        if serializer.is_valid():  # Check if data is valid
            serializer.save()  # Save the user to the database
            return Response({
                'message': 'User registered successfully',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

# Endpoint for user login
class LoginView(APIView):
    permission_classes = [AllowAny]  
    
    def post(self, request):
        username = request.data.get('username')  # Extract username from request
        password = request.data.get('password')  # Extract password from request

        # Validate presence of username and password
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # Log the user in
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

# Endpoint for user logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

    def post(self, request):
        try:
            logout(request)  # Log out the user
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:  # Handle unexpected errors
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Viewset for User Management (CRUD operations)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]