from django.urls import path
from . import views

urlpatterns = [
    path('', views.update_schedule, name='update_schedule'),
]