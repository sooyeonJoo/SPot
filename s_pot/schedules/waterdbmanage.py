from datetime import timedelta
from mobiles.models import Wateringcalendar, Wateringschedule,Plants

def save_watering_data_and_schedule_update(plants_id, start_date):
    # Wateringcalendar에 오늘 날짜 데이터 저장 부분을 제거하고,
    # 바로 start_date부터 물 주기 일정 생성
    userid=2

    # 물 주기 간격 (예: 4일)
    plant = Plants.objects.get(plantsid=plants_id)
    watering_interval = plant.wateringInterval


    schedules = []
    next_schedule_date = start_date

    # 물 주기 간격에 맞춰 4개의 날짜를 계산
    for _ in range(4):
        schedules.append(Wateringschedule(
            plantsid_id=plants_id,  # plantsid_id로 숫자 값 전달
            userid_id=userid,  # user_id로 숫자 값 전달
            date=next_schedule_date
        ))
        next_schedule_date += timedelta(days=watering_interval)

    # 중복 날짜 제거 후 스케줄 추가
    existing_dates = Wateringschedule.objects.filter(
        plantsid_id=plants_id,
        userid_id=userid,
        date__in=[schedule.date for schedule in schedules]
    ).values_list('date', flat=True)

    filtered_schedules = [schedule for schedule in schedules if schedule.date not in existing_dates]
    Wateringschedule.objects.bulk_create(filtered_schedules)

    print(f"새로운 스케줄 {len(filtered_schedules)}개를 추가했습니다.")
