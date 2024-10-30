from datetime import timedelta
from django.shortcuts import render

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from project_center.models import Project
from .models import Device, ServicePage, HourlyRate, CalendarSettings, ProjectCalendarSettings
from .serializers import  DeviceSerializer, ServicePageSerializer, HourlyRateSerializer, CalendarSettingsSerializer, ProjectCalendarSettingsSerializer

from rest_framework.permissions import DjangoModelPermissions, AllowAny
from rest_framework.exceptions import NotFound

from django.db.models import Q

class ProjectCalendarSettingsView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return ProjectCalendarSettings.objects.all()

    def get(self, request, format=None):
        settings = self.get_queryset().first()
        if settings is None:
            settings = ProjectCalendarSettings.objects.create()
        serializer = ProjectCalendarSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request, format=None):
        settings = self.get_queryset().first()
        serializer = ProjectCalendarSettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectOccupiedDatesView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Project.objects.filter(Q(status='activo') | Q(status='pausado'))

    def get(self, request, format=None):
        projects = self.get_queryset()
        occupied_dates = []
        for project in projects:
            start_date = project.start_date.date()
            end_date = project.finished_date.date()
            while start_date <= end_date:
                occupied_dates.append(start_date)
                start_date += timedelta(days=1)
        return Response(occupied_dates)


class OccupiedDatesView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Device.objects.filter(Q(device_status='en_reparacion') | Q(device_status='reparado'))

    def get(self, request, format=None):
        devices = self.get_queryset()
        occupied_dates = []
        for device in devices:
            start_date = device.start_date.date()
            end_date = device.finished_date.date()
            while start_date <= end_date:
                occupied_dates.append(start_date)
                start_date += timedelta(days=1)
        return Response(occupied_dates)

class CalendarSettingsView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return CalendarSettings.objects.all()

    def get(self, request, format=None):
        settings = self.get_queryset().first()
        if settings is None:
            settings = CalendarSettings.objects.create() 
        serializer = CalendarSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request, format=None):
        settings = self.get_queryset().first()
        if settings is None:
            return Response({"detail": "Settings not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CalendarSettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        code = request.query_params.get('code', None)
        if code is None:
            return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            device = Device.objects.get(unique_code=code)
            serializer = DeviceSerializer(device)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

class DeviceList(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Device.objects.all()

    def get(self, request, format=None):
        devices = self.get_queryset() 
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceDetail(APIView):

    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Device.objects.all()
    
    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Device.DoesNotExist:
            raise NotFound(detail="Objeto no encontrado", code=404)

    def get(self, request, pk, format=None):
        device = self.get_object(pk)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        device = self.get_object(pk)
        serializer = DeviceSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        device = self.get_object(pk)
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ServicePageList(APIView):

    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return ServicePage.objects.all()
    
    def get(self, request, format=None):
        servicePages = self.get_queryset() 
        serializer = ServicePageSerializer(servicePages, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ServicePageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServicePageDetail(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return ServicePage.objects.all()

    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except ServicePage.DoesNotExist:
            raise NotFound(detail="Objeto no encontrado", code=404)

    def get(self, request, pk, format=None):
        servicePage = self.get_object(pk)
        serializer = ServicePageSerializer(servicePage)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        servicePage = self.get_object(pk)
        serializer = ServicePageSerializer(servicePage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        servicePage = self.get_object(pk)
        servicePage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class HourlyRateView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return HourlyRate.objects.all()

    def get(self, request, format=None):
        hourly_rate = self.get_queryset().first()
        if hourly_rate:
            serializer = HourlyRateSerializer(hourly_rate)
            return Response(serializer.data)
        return Response({"rate": 0}, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        hourly_rate = self.get_queryset().first()
        if hourly_rate:
            serializer = HourlyRateSerializer(hourly_rate, data=request.data)
        else:
            serializer = HourlyRateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ARCHIVO PDF
    
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import ServicePage

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def generate_service_pdf(request, service_id):
    # Configura el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="service_{service_id}.pdf"'

    # Crear un canvas para dibujar el PDF
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Logotipo
    logo_path = 'operations/static/images/logo.png'  
    logo = ImageReader(logo_path)
    c.drawImage(logo, 40, height - 120, width=80, height=80)  

    # Título de la empresa 
    c.setFont("Helvetica-Bold", 40)
    title = "UMBRELLA-BITS"
    title_width = c.stringWidth(title, "Helvetica-Bold", 35)
    c.drawString((width - title_width) / 2, height - 100, title)

    # Datos del servicio
    service = ServicePage.objects.get(id=service_id)

    # Título del proyecto 
    c.setFont("Helvetica-Bold", 18)
    project_title = "Detalles del servicio del proyecto"
    project_title_width = c.stringWidth(project_title, "Helvetica-Bold", 18)
    c.drawString((width - project_title_width) / 2, height - 200, project_title)

    # Nombre del proyecto 
    c.setFont("Helvetica", 16)
    project_name = f'"{service.project.name}"'
    project_name_width = c.stringWidth(project_name, "Helvetica", 16)
    c.drawString((width - project_name_width) / 2, height - 230, project_name)

    offset = 280  

    # Detalle secciones con títulos
    details = [
        ("Descripción", service.description),
        ("Horas invertidas", f"{service.inverted_hours} horas"),
        ("Costos materiales", f"${service.material_cost}"),
        ("Costo total", f"${service.total_cost}")
    ]

    for title, value in details:
        c.setFont("Helvetica-Bold", 16)
        title_width = c.stringWidth(title, "Helvetica-Bold", 16)
        c.drawString((width - title_width) / 2, height - offset, title)

        c.setFont("Helvetica", 16)
        value_width = c.stringWidth(value, "Helvetica", 16)
        c.drawString((width - value_width) / 2, height - offset - 20, value)
        offset += 100

    c.showPage()
    c.save()
    return response