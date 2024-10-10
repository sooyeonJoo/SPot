from django.urls import path
from . import views

urlpatterns = [
   path('api/plants/<str:plant_name>/', views.crawl_plant_info, name='crawl_plant_info'),
]
