from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

# Create your models here.
User = get_user_model()

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks') # linking task to the user
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    priority_level = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium') # task priority
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending') # task status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # Timestamp when marked as complete

    def save(self, *args, **kwargs):
        # Set completed_at when status changes to "Completed"
        if self.status == 'Completed' and not self.completed_at:
            self.completed_at = datetime.now()
        # Reset completed_at if status is reverted to "Pending"
        elif self.status == 'Pending' and self.completed_at:
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title # string representation of a task