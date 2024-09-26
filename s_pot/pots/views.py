from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
import requests
import subprocess


# Create your views here.
@csrf_exempt  # CSRF 검증 비활성화
def control_pump(request):
    # 펌프
    if request.method == 'POST':
        esp32_url = "http://192.168.100.93/pump"  # ESP32 주소
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
            # 센서 값 처리
            print(f"Received sensor value: {sensor_value}")
            

            # # 특정 값을 지났을 때 waterdbmanage.py 실행
            # if sensor_value < 1000:  
            #     subprocess.run(["python", "../../schedules/waterdbmanage.py"])

    return JsonResponse({'sensor_value': sensor_value})

