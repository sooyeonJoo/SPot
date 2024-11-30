from django.http import JsonResponse
from .scheduler import update_scheduler_time  # scheduler.py의 함수 임포트
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_schedule(request):
    """
    클라이언트로부터 받은 시간에 맞춰 스케줄을 업데이트.
    """
    if request.method == "POST":
        try:
            # 디버그 메시지 추가
            print("Received POST request to update schedule.")

            # 클라이언트에서 전달받은 시간 (hour, minute)
            hour = request.GET.get("hour")
            minute = request.GET.get("minute")

            # hour, minute 유효성 검사
            if hour is None or minute is None:
                raise ValueError("Hour and minute parameters are required.")

            # int로 변환
            hour = int(hour)
            minute = int(minute)

            # 디버그 메시지
            print(f"Updating schedule to {hour}:{minute}")

            # 스케줄 업데이트 함수 호출
            update_scheduler_time(hour, minute)

            return JsonResponse({"status": "success", "message": "Schedule updated."})
        except Exception as e:
            print(f"Error while updating schedule: {e}")  # 예외 로그 출력
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)
