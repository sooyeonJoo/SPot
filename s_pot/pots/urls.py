from django.urls import path
from . import views

urlpatterns = [
    path('', views.control_pump, name='control_pump'),
]
