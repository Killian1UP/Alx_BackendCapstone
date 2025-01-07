from rest_framework import serializers
from .models import TaskHistory

class TaskHistorySerializer(serializers.ModelSerializer):
    # Added the nested fields to add more context about the task and the user in the response
    task_title = serializers.CharField(source='task.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TaskHistory
        fields = [
            'id',
            'task',
            'task_title',
            'action',
            'timestamp',
            'changes',
            'user',
            'user_username',
        ]
        read_only_fields = ['task', 'action', 'timestamp', 'changes', 'user']