from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.login_user, name='login_user'),
    path('api/join/', views.join_user, name='join_user'),
    path('api/plants/crawl/<str:plant_name>/', views.crawl_plant_info, name='crawl_plant_info'),
    path('api/plants/',views.get_plants, name='get_plants'),
    path('api/getPlantInfo/',views.get_plant_info, name='get_plant_info'),

    #등록하기 endpoint부분
    path('api/sendPlantData/', views.send_plant_data, name='send_plant_data'),
    path('api/sendWaterSchduleData/', views.send_watering_schedule, name='send_watering_schedule'),
    path('api/getWateringFrequency/<str:plant_name>/', views.get_watering_frequency, name='get_watering_frequency'),

]
