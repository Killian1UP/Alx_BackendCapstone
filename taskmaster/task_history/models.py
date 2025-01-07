from django.db import models
from tasks.models import Task
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class TaskHistory(models.Model):
    ACTION_CHOICES = [
        ('Created', 'Created'),
        ('Updated', 'Updated'),
        ('Completed', 'Completed'),
    ]
    # ForeignKey to the Task model, so each history record is linked to a specific task.
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    # JSONField to store any changes made to the task. It can store a list or dictionary of changes in JSON format.
    changes = models.JSONField(blank=True, null=True)
    # ForeignKey to the User model, linking the history entry to the user who made the change.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_histories')

    # String representation method to return a human-readable string for the history entry
    def __str__(self):
        return f"{self.action} - {self.task.title} - {self.timestamp}"