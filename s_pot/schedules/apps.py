from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

class SchedulesConfig(AppConfig):
    name = 'schedules'

    def ready(self):
        from .scheduler import check_plant_watering
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            check_plant_watering,
            'cron',
            hour=8,  # 매일 오전 8시에 실행
            minute=10
        )
        scheduler.start()
        print("Scheduler started")
