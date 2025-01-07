from django.urls import path
from .views import TaskHistoryListView

urlpatterns = [
    path('', TaskHistoryListView.as_view(), name='task-history'),
]