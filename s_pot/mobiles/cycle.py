import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 's_pot.settings')
django.setup()

from mobiles.models import Plants, Wateringschedule, User
from datetime import datetime, timedelta

def create_watering_schedule():
    user_id_input = input("사용자 ID를 입력하세요: ")  # 사용자 ID 입력
    try:
        user = User.objects.get(id=user_id_input)
    except User.DoesNotExist:
        print("사용자를 찾을 수 없습니다.")
        return

    plant_name = input("식물 이름을 입력하세요: ")
    start_date_input = input("시작 날짜를 입력하세요 (YYYY-MM-DD 형식): ")

    # 입력된 날짜를 datetime 객체로 변환
    start_date = datetime.strptime(start_date_input, "%Y-%m-%d").date()

    try:
        plant = Plant   s.objects.get(nickname=plant_name)
    except Plants.DoesNotExist:
        print("식물을 찾을 수 없습니다.")
        return

    watering_interval = plant.wateringInterval

    # 스케줄을 생성
    for i in range(0, 3):  # 3개의 스케줄 생성
        schedule_date = start_date + timedelta(days=i * watering_interval)
        Wateringschedule.objects.create(plantid=plant, userid=user, date=schedule_date)
        print(f"스케줄 생성: 식물: {plant.nickname}, 날짜: {schedule_date}")

if __name__ == "__main__":
    create_watering_schedule()
