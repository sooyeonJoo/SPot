from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def control_pump(request):
    # 펌프
    if request.method == 'POST':
        esp32_url = "http://192.168.0.51/pump"  # ESP32 주소
        try:
            response = requests.get(esp32_url)
            if response.status_code == 200:
                message = "Pump activated successfully!"
            else:
                message = f"Failed to activate pump: {response.status_code}"
        except requests.exceptions.RequestException as e:
            message = f"Error occurred: {e}"
        return render(request, 'control_pump.html', {'message': message})
        
    # 수분 센서
    sensor_url = "http://192.168.154.93/sensor"  # ESP32 주소
    try:
        sensor_response = requests.get(sensor_url)
        sensor_value = sensor_response.text
    except requests.exceptions.RequestException as e:
        sensor_value = f"Error occurred: {e}"
    context = {
        'sensor_value': sensor_value
    }

    return render(request, 'control_pump.html')
