import requests
from mobiles.models import Plants, Wateringschedule
from datetime import date

def check_plant_watering():
    print("Executing check_plant_watering...")  # 함수 실행 확인 로그
    today = date.today()
    schedules = Wateringschedule.objects.filter(date=today)

    if schedules.exists():
        plant_ids = schedules.values_list('plantid', flat=True)
        plants = Plants.objects.filter(plantsid__in=plant_ids)

        for plant in plants:
            print(f"오늘 물을 줘야 하는 식물: {plant.nickname}")
        
        try:
            response = requests.post('http://localhost:8000/pots/')
            if response.status_code == 200:
                print("펌프가 성공적으로 작동되었습니다.")
            else:
                print(f"펌프 작동 실패: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"에러 발생: {e}")
    else:
        print("오늘 물을 줄 식물이 없습니다.")

