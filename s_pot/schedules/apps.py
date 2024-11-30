from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'schedules'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()  # 서버 시작 시 스케줄러 시작cd