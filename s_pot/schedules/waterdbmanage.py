from django.utils import timezone
from datetime import timedelta
from mobiles.models import Wateringcalendar, Wateringschedule

def save_watering_data_and_schedule_update(plant, user, start_date, watering_interval):
    print("save_watering_data_and_schedule_update")
    current_date = timezone.now().date()

    # Wateringcalendar에 오늘 날짜 데이터 저장
    watering_entry = Wateringcalendar.objects.create(
        plantid=plant,
        userid=user,
        date=current_date
    )
    watering_entry.save()

    # 첫 번째 스케줄을 기준으로 한 달치 스케줄 생성
    schedule_start_date = start_date  # 사용자가 입력한 시작 날짜
    schedules = []
    
    # 한 달간 물 주기 스케줄을 생성
    for i in range(30):  # 한 달간 반복
        next_schedule_date = schedule_start_date + timedelta(days=(i * watering_interval))
        schedules.append(Wateringschedule(
            plantid=plant,
            userid=user,
            date=next_schedule_date
        ))

    # 이미 존재하는 스케줄과 겹치는 날짜를 필터링하여 추가
    existing_dates = Wateringschedule.objects.filter(
        plantid=plant, userid=user, date__in=[schedule.date for schedule in schedules]
    ).values_list('date', flat=True)

    filtered_schedules = [schedule for schedule in schedules if schedule.date not in existing_dates]

    # 새로운 스케줄 추가
    Wateringschedule.objects.bulk_create(filtered_schedules)

    print(f"새로운 스케줄 {len(filtered_schedules)}개를 추가했습니다.")
