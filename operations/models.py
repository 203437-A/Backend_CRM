from django.db import models

# Create your models here.
from users.models import Client
from project_center.models import Project
import uuid


class Device(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    device_status = models.CharField(max_length=20, choices=[('en_reparacion', 'En reparación'), ('reparado', 'Reparado'), ('entregado', 'Entregado')])
    start_date = models.DateTimeField(null=False, blank=False)
    finished_date = models.DateTimeField(null=False, blank=False)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ServicePage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    inverted_hours = models.FloatField()
    material_cost = models.FloatField()
    total_cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HourlyRate(models.Model):
    rate = models.FloatField()

    def __str__(self):
        return f"Rate: {self.rate}"
    
class CalendarSettings(models.Model):
    allow_weekends = models.BooleanField(default=False)
    start_hour = models.TimeField(default="08:00")
    end_hour = models.TimeField(default="16:00")

class ProjectCalendarSettings(models.Model):
    allow_weekends = models.BooleanField(default=False)
    start_hour = models.TimeField(default="08:00")
    end_hour = models.TimeField(default="16:00")


