import os
import socket

# 현재 시스템의 IP 주소 가져오기
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Django 서버 실행
os.system(f"python manage.py runserver {local_ip}:8000")