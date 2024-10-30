from django.urls import path
from .views import ProjectList, ProjectDetail,TaskList, TaskDetail



urlpatterns = [
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<int:project_id>/', TaskList.as_view(), name='project-task-list'),
    path('tasks/detail/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
]
