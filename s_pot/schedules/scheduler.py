from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .scheduler_tasks import check_plant_watering

scheduler = BackgroundScheduler()

# 스케줄러 시작
def start_scheduler():
    if len(scheduler.get_jobs()) == 0:
        print("Scheduler started.")
        scheduler.add_job(
            check_plant_watering,
            'cron',
            hour=11,
            minute=11
        )
        scheduler.start()

from apscheduler.triggers.cron import CronTrigger

def update_scheduler_time(hour, minute):
    print("Updating scheduler...")
    jobs = scheduler.get_jobs()
    print(f"Current jobs: {jobs}")  # 현재 등록된 작업 출력

    # 모든 기존 작업 제거
    if jobs:
        for job in jobs:
            print(f"Removing job: {job}")
            scheduler.remove_job(job.id)

    # 새 작업 추가
    trigger = CronTrigger(hour=hour, minute=minute)
    scheduler.add_job(
        check_plant_watering,
        trigger=trigger,
        id="check_plant_watering"  # 같은 ID를 사용해 중복 추가 방지
    )
    print(f"New job added at {hour}:{minute}")

