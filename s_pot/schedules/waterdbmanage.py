from django.utils import timezone
from datetime import timedelta
from mobiles.models import Wateringcalendar, Wateringschedule

print("waterdbmanage.py executed successfully.")

def save_watering_data_and_schedule_update(plant, user):
    print("save_watering_data_and_schedule_update")
    current_date = timezone.now().date()

    watering_entry = Wateringcalendar.objects.create(
        plantid=plant,
        userid=user,
        date=current_date
    )
    watering_entry.save()

    first_scheduled_entry = Wateringschedule.objects.filter(plantid=plant, userid=user).order_by('date').first()

    watering_interval = plant.wateringInterval

    if first_scheduled_entry:
        first_scheduled_date = first_scheduled_entry.date
        print(f"가장 최근의 스케줄 날짜: {first_scheduled_date}")

        schedule_1 = first_scheduled_date + timedelta(days=watering_interval)
        schedule_2 = schedule_1 + timedelta(days=watering_interval)
        schedule_3 = schedule_2 + timedelta(days=watering_interval)
    else:
        print("스케줄이 없으므로 오늘 날짜를 기준으로 계산합니다.")
        schedule_1 = current_date + timedelta(days=watering_interval)
        schedule_2 = schedule_1 + timedelta(days=watering_interval)
        schedule_3 = schedule_2 + timedelta(days=watering_interval)

    new_schedules = [
        Wateringschedule(plantid=plant, userid=user, date=schedule_1),
        Wateringschedule(plantid=plant, userid=user, date=schedule_2),
        Wateringschedule(plantid=plant, userid=user, date=schedule_3),
    ]

    existing_dates = Wateringschedule.objects.filter(
        plantid=plant, userid=user, date__in=[schedule_1, schedule_2, schedule_3]
    ).values_list('date', flat=True)

    filtered_schedules = [schedule for schedule in new_schedules if schedule.date not in existing_dates]

    Wateringschedule.objects.bulk_create(filtered_schedules)

    print(f"새로운 스케줄 {len(filtered_schedules)}개를 추가했습니다.")
