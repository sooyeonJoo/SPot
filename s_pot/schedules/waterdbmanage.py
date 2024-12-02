from django.utils import timezone
from datetime import timedelta
from mobiles.models import Wateringcalendar, Wateringschedule, Plants
from rest_framework.response import Response
from rest_framework import status

def save_watering_data_and_schedule_update(plant, start_date):
    print("save_watering_data_and_schedule_update")
    current_date = timezone.now().date()

    # 고정된 사용자 ID
    user_id = 2  # 하드코딩된 사용자 ID

    # Wateringcalendar에 오늘 날짜 데이터 저장
    try:
        Wateringcalendar.objects.create(
            plantsid=plant,  # plantid를 plantsid로 수정
            userid_id=user_id,  # user 객체 대신 고정된 ID 사용
            date=current_date
        )
    except Exception as e:
        print(f"Wateringcalendar 저장 오류: {str(e)}")
        raise e  # 예외 발생시키기

    # `plant` 객체에서 wateringInterval 값을 명시적으로 가져오기
    watering_interval = plant.wateringInterval  # plant 객체에서 직접 가져오기

    # 시작 날짜부터 주기 간격에 맞춰 스케줄 생성
    schedules = []
    next_schedule_date = start_date

    # 최대 4개 스케줄만 생성
    for _ in range(4):
        schedules.append(Wateringschedule(
            plantsid=plant,
            userid_id=user_id,  # user 객체 대신 고정된 ID 사용
            date=next_schedule_date
        ))
        next_schedule_date += timedelta(days=watering_interval)  # 물 주기 간격 추가

    # 이미 존재하는 스케줄과 겹치는 날짜를 필터링하여 추가
    existing_dates = Wateringschedule.objects.filter(
        plantsid=plant,
        userid_id=user_id,
        date__in=[schedule.date for schedule in schedules]
    ).values_list('date', flat=True)

    # 기존 스케줄과 겹치지 않는 새로운 스케줄만 필터링
    filtered_schedules = [schedule for schedule in schedules if schedule.date not in existing_dates]

    # 새로운 스케줄 추가
    try:
        Wateringschedule.objects.bulk_create(filtered_schedules)
    except Exception as e:
        print(f"스케줄 저장 오류: {str(e)}")
        raise e  # 예외 발생시키기

    print(f"새로운 스케줄 {len(filtered_schedules)}개를 추가했습니다.")
