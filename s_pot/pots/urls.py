from django.urls import path
from . import views

urlpatterns = [
    path('', views.control_pump, name='control_pump'),
    path('control_sensorData/', views.control_sensorData, name='control_sensorData'),
]
