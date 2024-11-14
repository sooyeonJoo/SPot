from django.views.decorators.csrf import csrf_exempt
from mobiles.models import Plants, User
from django.shortcuts import render
from django.http import JsonResponse
import requests
import importlib


# Create your views here.
@csrf_exempt  # CSRF 검증 비활성화
def control_pump(request):
    # 펌프
    if request.method == 'POST':
        esp32_url = "http://192.168.135.93/pump"  # ESP32 주소
        try:
            response = requests.get(esp32_url)
            if response.status_code == 200:
                message = "Pump activated successfully!"
            else:
                message = f"Failed to activate pump: {response.status_code}"
        except requests.exceptions.RequestException as e:
            message = f"Error occurred: {e}"
        return render(request, 'control_pump.html', {'message': message})

    return render(request, 'control_pump.html')



@csrf_exempt  # CSRF 검증 비활성화
def control_sensorData(request):
    # 센서 데이터 수신 (POST 요청)
    if request.method == 'POST':
        sensor_value = request.POST.get('sensor_value', None)  # 센서 값 가져오기
        
        if sensor_value is not None:
            try:
                sensor_value = int(sensor_value)  # 문자열을 정수로 변환
            except ValueError:
                return JsonResponse({'error': 'Invalid sensor value'}, status=400)

            # 센서 값 처리
            print(f"Received sensor value: {sensor_value}")

            response_data = {'sensor_value': sensor_value}

            # # 특정 값 미만일 때 waterdbmanage.py 실행
            # if sensor_value < 1000:  
            #     importlib.import_module('schedules.waterdbmanage')
            #     response_data['message'] = 'waterdbmanage.py 실행 완료'

            # 특정 값 미만일 때 waterdbmanage.py 실행
            if sensor_value < 1000:
                waterdbmanage = importlib.import_module('schedules.waterdbmanage')
                
                plant_instance = Plants.objects.get(plantsid = 1) 
                user_instance = User.objects.get(userid = 1) 
                waterdbmanage.save_watering_data_and_schedule_update(plant_instance, user_instance)

                response_data['message'] = 'save_watering_data_and_schedule_update 함수 실행 완료'


            return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

