import os
from get_wifi_ip import get_wifi_ip

# Wi-Fi의 IPv4 주소 가져오기
local_ip = get_wifi_ip()

if local_ip:
    # Django 서버 실행
    os.system(f"python manage.py runserver {local_ip}:8000")
else:
    print("Wi-Fi IPv4 주소를 찾을 수 없습니다.")