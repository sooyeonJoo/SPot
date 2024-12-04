import os
import requests
from django.core.files import File
from .models import PlantsInfo
from django.conf import settings
from tempfile import NamedTemporaryFile

def download_image_to_media(plant_info):
    image_url = plant_info.image_url  # 기존 image_url을 사용
    response = requests.get(image_url)
    
    if response.status_code == 200:
        # 임시 파일 생성, 삭제하지 않음
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file.seek(0)  # 파일을 읽을 준비
            # 임시 파일을 model의 image 필드에 저장
            plant_info.image.save(os.path.basename(image_url), File(temp_file))
            plant_info.save()
