from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom manager to handle user creation logic
class CustomUserManager(BaseUserManager):
    # Method to create a standard user
    def create_user(self, username, email, password=None):
        if not email:  # Ensure email is provided
            raise ValueError("Users must have an email address")
        if not username:  # Ensure username is provided
            raise ValueError("Users must have a username")
        
        email = self.normalize_email(email)  # Normalize email to a standard format
        user = self.model(username=username, email=email)  # Create user instance
        user.set_password(password)  # Hash and set the password
        user.save(using=self._db)  # Save the user to the database
        return user

    # Method to create a superuser with admin privileges
    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True  # Set admin privileges
        user.save(using=self._db)
        return user

# Custom user model extending AbstractBaseUser
class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)  # Unique username field
    email = models.EmailField(unique=True)  # Unique email field
    is_active = models.BooleanField(default=True)  # Status to track if user is active
    is_admin = models.BooleanField(default=False)  # Admin privileges flag

    objects = CustomUserManager()  # Assign custom manager

    # Field used as the unique identifier for authentication
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Fields required to create a user

    def __str__(self):
        return self.username  # String representation of the user

    # Permissions handling for admin users
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Module-level permissions for admin users
    def has_module_perms(self, app_label):
        return self.is_admin