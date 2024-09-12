
def check_plant_watering():
    from mobiles.models import Plants, Wateringschedule
    from datetime import date

    today = date.today()
    schedules = Wateringschedule.objects.filter(date=today)
    if schedules.exists():
        plant_ids = schedules.values_list('plantid', flat=True)
        plants = Plants.objects.filter(plantsid__in=plant_ids)
        for plant in plants:
            print(f"오늘 물을 줘야 하는 식물: {plant.nickname}")
    else:
        print("오늘 물을 줄 식물이 없습니다.")