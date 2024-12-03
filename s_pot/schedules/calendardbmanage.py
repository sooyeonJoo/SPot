from datetime import timedelta
from django.utils import timezone
from mobiles.models import Wateringcalendar, Wateringschedule, Plants

def schedule_update(plants_id, user_id):
    # 현재 날짜 가져오기 (물 주는 날짜)
    today = timezone.now().date()
    plant = Plants.objects.get(plantsid=plants_id)
    watering_interval = plant.wateringInterval  # 물주기 간격

    # 1. Wateringcalendar 테이블에 물주기 기록 추가
    Wateringcalendar.objects.create(
        plantsid=plants_id,
        userid=user_id,
        date=today
    )

    # 2. Wateringschedule에서 가장 빠른 날짜 찾기
    earliest_schedule = Wateringschedule.objects.filter(plantsid=plants_id).order_by('date').first()

    # 3. 물주기 일정 처리
    if earliest_schedule:
        if earliest_schedule.date == today:
            # 기존 일정 삭제 (기존 일정이 오늘 날짜와 같으면 삭제)
            earliest_schedule.delete()

            # 가장 늦은 날짜 가져오기
            latest_schedule = Wateringschedule.objects.filter(plantsid=plants_id).order_by('-date').first()
            latest_date = latest_schedule.date if latest_schedule else today  # 없으면 오늘 날짜 사용

            # 새로운 물주기 날짜 계산 (가장 늦은 날짜 + wateringInterval)
            new_date = latest_date + timedelta(days=watering_interval)

            # 새로운 일정 추가
            Wateringschedule.objects.create(
                plantsid=plants_id,
                userid=user_id,
                date=new_date
            )

        else:
            # 가장 빠른 날짜가 오늘과 다를 경우 기존 일정 삭제
            Wateringschedule.objects.filter(plantsid=plants_id).delete()

            # 새로운 일정 계산: 오늘부터 시작해서 wateringInterval 간격으로 일정 생성
            new_dates = [today + timedelta(days=watering_interval * i) for i in range(4)]  # 4개 일정 생성

            # 새로 생성한 일정들을 Wateringschedule 테이블에 추가
            new_schedules = [
                Wateringschedule(plantsid=plants_id, userid=user_id, date=date)
                for date in new_dates
            ]
            Wateringschedule.objects.bulk_create(new_schedules)

    else:
        # 일정이 아예 없는 경우, 오늘 날짜부터 4일 간격으로 일정 생성
        new_dates = [today + timedelta(days=watering_interval * i) for i in range(4)]  # 4개 일정 생성

        # 새로 생성한 일정들을 Wateringschedule 테이블에 추가
        new_schedules = [
            Wateringschedule(plantsid=plants_id, userid=user_id, date=date)
            for date in new_dates
        ]
        Wateringschedule.objects.bulk_create(new_schedules)
