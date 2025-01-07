from rest_framework import serializers
from .models import Task
from datetime import date

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']  # Make user read-only so it's auto-assigned

    # validation for due_date
    def validate_due_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    # validation for priority_level
    def validate_priority_level(self, value):
        valid_priorities = ['Low', 'Medium', 'High']
        if value not in valid_priorities:
            raise serializers.ValidationError(f"Priority level must be one of {valid_priorities}.")
        return value

    # validation for status
    def validate_status(self, value):
        valid_statuses = ['Pending', 'Completed']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}.")
        return value

    def validate(self, data):
        # Prevent editing tasks marked as Completed
        if self.instance and self.instance.status == 'Completed' and data.get('status') != 'Pending':
            raise serializers.ValidationError("Completed tasks cannot be edited unless reverted to 'Pending'.")
        return data
    
    def create(self, validated_data):
        # Automatically assign the authenticated user to the task
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)