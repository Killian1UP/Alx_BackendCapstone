from django.urls import path
from . import views

urlpatterns = [
    # CRUD operation endpoints for Task Management
    path('', views.TaskListView.as_view(), name='task_list'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('new/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    # Status endpoint
    path('<int:pk>/status/', views.TaskStatusUpdateView.as_view(), name='task_status'),
]