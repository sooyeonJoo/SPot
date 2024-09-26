
from django.utils import timezone
from mobiles.models import Wateringcalendar, Wateringschedule, Plants, User

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

    # WateringSchedule에서 해당 plant 및 user에 대한 첫 번째 날짜 가져오기
    first_scheduled_entry = Wateringschedule.objects.filter(plantid=plant, userid=user).order_by('date').first()

    # 첫 번째 스케줄 날짜 가져오기
    if first_scheduled_entry:
        scheduled_date = first_scheduled_entry.date  # WateringSchedule의 첫 번째 날짜
        
        # 현재 날짜와 첫 번째 스케줄 날짜 비교
        if current_date == scheduled_date:
            first_scheduled_entry.delete()
            print(f"현재 날짜({current_date})와 첫 번째 스케줄({scheduled_date})가 같아서 삭제했습니다.")
            
            # Plants 테이블에서 wateringInterval 값 가져오기
            watering_interval = Plants.wateringInterval  # 물 주기 (예: 7일)
            
            # 새로운 날짜 계산
            new_scheduled_date = current_date + timezone.timedelta(days=watering_interval)

            # 새로운 WateringSchedule 레코드 추가
            new_schedule_entry = Wateringschedule.objects.create(
                plantid=plant,
                userid=user,
                date=new_scheduled_date
            )
            new_schedule_entry.save()

            print(f"새로운 스케줄을 추가했습니다: {new_scheduled_date}")

        else:
            print("현재 날짜가 아닙니다.")
    else:
        print("해당 사용자의 WateringSchedule 데이터가 없습니다.")
