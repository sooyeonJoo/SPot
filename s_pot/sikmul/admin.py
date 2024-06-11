from django.contrib import admin
from .models import BloomingSeason, Calender, CultivationSeason, DjangoMigrations, HarvestingSeason, Plants, PlantsInfo, User

@admin.register(BloomingSeason)
class BloomingSeasonAdmin(admin.ModelAdmin):
    list_display = ('plantsid', 'engname', 'season')

@admin.register(Calender)
class CalenderAdmin(admin.ModelAdmin):
    list_display = ('plantsid', 'userid', 'event_date', 'title', 'detail', 'user')

@admin.register(CultivationSeason)
class CultivationSeasonAdmin(admin.ModelAdmin):
    list_display = ('plantsid', 'engname', 'season')

@admin.register(DjangoMigrations)
class DjangoMigrationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'app', 'name', 'applied')

@admin.register(HarvestingSeason)
class HarvestingSeasonAdmin(admin.ModelAdmin):
    list_display = ('plantsid', 'engname', 'season')

@admin.register(Plants)
class PlantsAdmin(admin.ModelAdmin):
    list_display = ('plantsid', 'engname', 'lifespan', 'sepecies', 'cultivation_season', 'blooming_season', 'harvesting_season', 'temperature', 'sunlight', 'watering_frequency', 'pests_diseases')

@admin.register(PlantsInfo)
class PlantsInfoAdmin(admin.ModelAdmin):
    list_display = ('engname', 'blooming_season', 'cultivation_season', 'harvesting_season', 'watering_frequency', 'sunlight', 'temperature')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
     list_display = ('userid', 'id', 'passwd', 'name', 'birthday', 'gender', 'email')