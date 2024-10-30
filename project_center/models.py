from django.db import models

from users.models import Client, Employee

# Create your models here.

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    finished_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('completado', 'Completado'), ('pausado', 'Pausado')])
    manage_user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completa', 'Completa')])
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    finished_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

