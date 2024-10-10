from django.utils import timezone
from datetime import timedelta
from mobiles.models import Wateringcalendar, Wateringschedule, Plants

print("waterdbmanage.py executed successfully.")

def save_watering_data_and_schedule_update(plant, user):
    # 현재 날짜 가져오기
    current_date = timezone.now().date()

    # WateringCalendar에 데이터 저장
    watering_entry = Wateringcalendar.objects.create(
        plantid=plant,  # Plants 모델의 인스턴스
        userid=user,    # User 모델의 인스턴스
        date=current_date
    )
    watering_entry.save()

    # WateringSchedule에서 해당 plant 및 user에 대한 가장 최근 날짜 가져오기
    last_scheduled_entry = Wateringschedule.objects.filter(plantid=plant, userid=user).order_by('date').last()

    watering_interval = Plants.wateringInterval  # Plants 테이블에서 물 주기 값 (숫자)

    if last_scheduled_entry:
        # 마지막 스케줄의 날짜 가져오기
        last_scheduled_date = last_scheduled_entry.date
        print(f"가장 최근의 스케줄 날짜: {last_scheduled_date}")

        # 새로운 날짜 계산: 마지막 스케줄 날짜에 물 주기를 더한 날짜
        schedule_1 = last_scheduled_date + timedelta(days=watering_interval)
        schedule_2 = schedule_1 + timedelta(days=watering_interval)
        schedule_3 = schedule_2 + timedelta(days=watering_interval)

    else:
        # 스케줄이 없을 경우, 오늘 날짜 기준으로 스케줄 생성
        print("스케줄이 없으므로 오늘 날짜를 기준으로 계산합니다.")
        schedule_1 = current_date + timedelta(days=watering_interval)
        schedule_2 = schedule_1 + timedelta(days=watering_interval)
        schedule_3 = schedule_2 + timedelta(days=watering_interval)

    # 새로운 WateringSchedule 레코드 3개 추가
    Wateringschedule.objects.bulk_create([
        Wateringschedule(plantid=plant, userid=user, date=schedule_1),
        Wateringschedule(plantid=plant, userid=user, date=schedule_2),
        Wateringschedule(plantid=plant, userid=user, date=schedule_3),
    ])

    print(f"새로운 스케줄 3개를 추가했습니다: {schedule_1}, {schedule_2}, {schedule_3}")
