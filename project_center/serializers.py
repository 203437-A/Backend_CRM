
from rest_framework import serializers
from .models import  Project, Task
from users.models import Client
from users.models import Employee
import datetime


class ProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.first_name', read_only=True) 
    manage_user_name = serializers.CharField(source='manage_user.first_name', read_only=True) 
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    manage_user = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    start_date = serializers.DateTimeField()
    finished_date = serializers.DateTimeField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'start_date', 'finished_date', 'created_at', 'updated_at', 'client_name', 'client', 'status_display', 'manage_user', 'manage_user_name',]

    def get_status_display(self, obj):
        return obj.get_status_display()




class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    start_date = serializers.DateTimeField()
    finished_date = serializers.DateTimeField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'status', 'start_date', 'finished_date',
            'project', 'project_name', 'employee', 'employee_name', 'status_display'
        ]

    def get_status_display(self, obj):
        return obj.get_status_display()

