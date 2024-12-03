import os
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from .models import PlantsInfo

def download_image_to_media(plant_info):
    image_url = plant_info.image_url  # 기존 image_url을 사용
    response = requests.get(image_url)
    
    if response.status_code == 200:
        # 임시 파일로 이미지 저장
        image_file = NamedTemporaryFile(delete=False)
        image_file.write(response.content)
        image_file.close()
        
        # 해당 이미지를 모델의 image 필드에 저장
        plant_info.image.save(os.path.basename(image_url), File(image_file))
        plant_info.save()  # 모델 저장
