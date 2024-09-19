from django.contrib import admin
from .models import Calendar, Plants, PlantsInfo, User, Wateringcalendar, Wateringschedule

@admin.register(Calendar)
class CalenderAdmin(admin.ModelAdmin):
    list_display = ('calendarid','plantsid', 'event_date', 'title', 'detail', 'user', 'wateringdate')

@admin.register(Plants)
class PlantsAdmin(admin.ModelAdmin):
    list_display = ('plantsid', 'name', 'nickname', 'birthday', 'deathday', 'color','wateringInterval')

@admin.register(PlantsInfo)
class PlantsInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'engname', 'lifespan', 'sunlight', 'blooming_season', 'cultivation_season', 'harvesting_season', 'watering_frequency', 'temperature', 'pests_diseases')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'id', 'passwd', 'name', 'birthday', 'gender', 'tel', 'email')

@admin.register(Wateringcalendar)
class WateringcalendarAdmin(admin.ModelAdmin):
    list_display = ('plantid', 'userid', 'date')

@admin.register(Wateringschedule)
class WateringscheduleAdmin(admin.ModelAdmin):
    list_display = ('plantid', 'userid', 'date')