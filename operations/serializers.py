from rest_framework import serializers
from .models import Device, ServicePage, HourlyRate, CalendarSettings, ProjectCalendarSettings
from users.models import Client
from project_center.models import Project	

class DeviceSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.first_name', read_only=True) 
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    start_date = serializers.DateTimeField()
    finished_date = serializers.DateTimeField()
    device_status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Device
        fields = ['id', 'name', 'description', 'device_status', 'start_date', 'finished_date', 'created_at', 'updated_at', 'client_name', 'client', 'device_status_display', 'unique_code']

    def get_device_status_display(self, obj):
        return obj.get_device_status_display()


class ServicePageSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    class Meta:
        model = ServicePage
        fields = [
            'id', 'project', 'description', 'inverted_hours',
            'material_cost', 'total_cost', 'created_at', 'updated_at', 'project_name'
        ]

    def validate_inverted_hours(self, value):
        """
        Check that the inverted hours are not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Las horas invertidas no pueden ser negativas.")
        return value

    def validate_material_cost(self, value):
        """
        Check that the material cost is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("El costo de materiales no puede ser negativo.")
        return value

    def validate_total_cost(self, value):
        """
        Check that the total cost is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("El costo total no puede ser negativo.")
        return value

class HourlyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyRate
        fields = ['rate']

class CalendarSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarSettings
        fields = ['allow_weekends', 'start_hour', 'end_hour']

class ProjectCalendarSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCalendarSettings
        fields = ['allow_weekends', 'start_hour', 'end_hour']



