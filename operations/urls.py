from django.urls import path
from .views import DeviceList, DeviceDetail, ServicePageList, ServicePageDetail, generate_service_pdf, HourlyRateView, DeviceStatusView, CalendarSettingsView, OccupiedDatesView, ProjectCalendarSettingsView, ProjectOccupiedDatesView

urlpatterns = [
    path('devices/', DeviceList.as_view(), name='device-list'),
    path('devices/<int:pk>/', DeviceDetail.as_view(), name='device-detail'),
    path('device-status/', DeviceStatusView.as_view(), name='device-status'),
    path('services/', ServicePageList.as_view(), name='servicePage-list'),
    path('services/<int:pk>/', ServicePageDetail.as_view(), name='servicePage-detail'),
    path('services/<int:service_id>/pdf/', generate_service_pdf, name='service_pdf'),
    path('hourly-rate/', HourlyRateView.as_view(), name='hourly_rate'),
    path('calendar-settings/', CalendarSettingsView.as_view(), name='calendar-settings'),
    path('occupied-dates/', OccupiedDatesView.as_view(), name='occupied-dates'),
    path('project-calendar-settings/', ProjectCalendarSettingsView.as_view(), name='project-calendar-settings'),
    path('project-occupied-dates/', ProjectOccupiedDatesView.as_view(), name='project-occupied-dates'),
]
