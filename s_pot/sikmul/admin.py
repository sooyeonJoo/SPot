from django.contrib import admin
from .models import Calender, Plants, PlantsInfo, User

@admin.register(Calender)
class CalenderAdmin(admin.ModelAdmin):
    list_display = ('plantsid', 'userid', 'event_date', 'title', 'detail', 'user')

@admin.register(Plants)
class PlantsAdmin(admin.ModelAdmin):
    list_display = ('plantsid', 'name', 'nickname', 'birthday', 'deathday', 'color')

@admin.register(PlantsInfo)
class PlantsInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'engname', 'lifespan', 'sunlight', 'blooming_season', 'cultivation_season', 'harvesting_season', 'watering_frequency','temperature','pests_diseases')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
     list_display = ('userid', 'id', 'passwd', 'name', 'birthday', 'gender', 'tel','email')