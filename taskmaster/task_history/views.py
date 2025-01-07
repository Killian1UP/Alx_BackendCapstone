from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskHistorySerializer
from .models import TaskHistory
from rest_framework import generics
# Create your views here.
class TaskHistoryListView(generics.ListAPIView):
    serializer_class = TaskHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict the queryset to show only task history for tasks belonging to the authenticated user.
        return TaskHistory.objects.filter(task__user=self.request.user).order_by('-timestamp')
