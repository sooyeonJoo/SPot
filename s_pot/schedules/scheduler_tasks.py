import requests
from mobiles.models import Plants, Wateringschedule
from datetime import date

def check_plant_watering():
    print("Executing check_plant_watering...")  # 함수 실행 확인 로그
    today = date.today()
    schedules = Wateringschedule.objects.filter(date=today)

    if schedules.exists():
        plant_ids = schedules.values_list('plantsid', flat=True)
        plants = Plants.objects.filter(plantsid__in=plant_ids)

        for plant in plants:
            print(f"오늘 물을 줘야 하는 식물: {plant.nickname}")
        
        # ESP32에 직접 요청 보내기
        try:
            esp32_url = "http://192.168.0.51/pump"  # ESP32 주소
            response = requests.get(esp32_url)
            if response.status_code == 200:
                print("Pump activated successfully!")
            else:
                print(f"Failed to activate pump: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
    else:
        print("오늘 물을 줄 식물이 없습니다.")
