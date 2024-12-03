from mobiles.models import Plants, Wateringschedule
from datetime import date
from pots.views import activate_pump_directly

def check_plant_watering():
    print("Executing check_plant_watering...")  # 함수 실행 확인 로그
    today = date.today()
    schedules = Wateringschedule.objects.filter(date=today)

    if schedules.exists():
        plant_ids = schedules.values_list('plantsid', flat=True)
        plants = Plants.objects.filter(plantsid__in=plant_ids)

        for plant in plants:
            print(f"오늘 물을 줘야 하는 식물: {plant.nickname}")
        
        # activate_pump_directly 호출
        pump_result = activate_pump_directly()
        print(f"Pump activation result: {pump_result}")
    else:
        print("오늘 물을 줄 식물이 없습니다.")