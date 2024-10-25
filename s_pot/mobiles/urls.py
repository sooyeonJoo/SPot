from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.login_user, name='login_user'),
    #path('api/plants/<str:plant_name>/', views.crawl_plant_info, name='crawl_plant_info'),
    path('api/plants/crawl/<str:plant_name>/', views.crawl_plant_info, name='crawl_plant_info'),

]
