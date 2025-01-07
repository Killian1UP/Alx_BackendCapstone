from django.shortcuts import render
from rest_framework import generics, status
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from task_history.models import TaskHistory
from task_history.serializers import TaskHistorySerializer
# Create your views here.

class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'status', 'priority_level', 'due_date']
    search_fields = ['title']
    ordering_fields = ['due_date', 'priority_level']

    def get_queryset(self):
        # restricted tasks to the current user
        return Task.objects.filter(user=self.request.user)

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # restricted tasks to the current user
        return Task.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()
        task_history = TaskHistory.objects.filter(task=task)

        # Serialize the task and task history
        task_serializer = self.get_serializer(task)
        history_serializer = TaskHistorySerializer(task_history, many=True)

        return Response({
            'task': task_serializer.data,
            'task_history': history_serializer.data
        })

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # The validation ensures that the task's user field is automatically set to the currently authenticated user during creation.
        task = serializer.save(user=self.request.user)

        # Log the task creation in history
        TaskHistory.objects.create(
            task=task,
            action='Created',
            changes=None,  # or include a dictionary of task details if needed
            user=self.request.user
        )

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        # Get the task instance being updated
        task = self.get_object()

        # Create TaskHistory record for the update
        TaskHistory.objects.create(
            task=task,
            action='Updated',
            changes=self.get_task_changes(task, serializer),  # Implement this to track changes
            user=self.request.user
        )

        # Perform the update
        serializer.save()

    def get_task_changes(self, task, serializer):
        """
        A method to get the changes that were made to the task.
        You can track changes between the task and serializer data here.
        """
        changes = {}
        for field in serializer.validated_data:
            if getattr(task, field) != serializer.validated_data[field]:
                changes[field] = {
                    'old': getattr(task, field),
                    'new': serializer.validated_data[field]
                }
        return changes

class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)  # Ensure the task belongs to the current user
        except Task.DoesNotExist:
            return Response({'error': 'Task not found or does not belong to you.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status not in ['Pending', 'Completed']:
            return Response({'error': 'Invalid status. Valid statuses are Pending and Completed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update status and save
        task.status = new_status
        task.save()
        
        # Log the status change in task history
        TaskHistory.objects.create(
            task=task,
            action='Completed' if new_status == 'Completed' else 'Updated',  # Adjust depending on status
            changes={'status': task.status},
            user=request.user
        )

        return Response({'message': 'Task status updated successfully.', 'task': TaskSerializer(task).data}, status=status.HTTP_200_OK)
