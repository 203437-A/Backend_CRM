from django.shortcuts import render

# Create your views here.

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import NotFound


class ProjectList(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Project.objects.all()

    def get(self, request, format=None):
        projects = self.get_queryset()  
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Project.objects.all()
    
    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound(detail="Objeto no encontrado", code=404)

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TaskList(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self, project_id=None):
        if project_id:
            return Task.objects.filter(project__id=project_id)
        return Task.objects.all()
    
    def get(self, request, project_id=None, format=None):
        tasks = self.get_queryset(project_id)  
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):

    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Task.objects.all()
    
    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound(detail="Objeto no encontrado", code=404)

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    