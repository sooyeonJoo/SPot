
import os
import requests
from django.core.files import File
from .models import PlantsInfo
from django.conf import settings
from tempfile import NamedTemporaryFile

def download_image_to_media(plant_info):
    image_url = plant_info.image_url  # 크롤링한 이미지 URL을 사용

    # 절대경로 URL이 아닌 경우 상대경로가 올 수 있으므로 처리
    if not image_url.startswith("http"):
        image_url = settings.BASE_URL + image_url  # BASE_URL을 설정하여 절대 URL로 변경
    
    # 확장자가 없을 경우 기본 확장자 추가
    if not image_url.endswith(('jpg', 'jpeg', 'png', 'gif')):
        image_url += '.jpg'  # 예시로 .jpg를 기본 추가

    response = requests.get(image_url)
    if response.status_code == 200:
        # 임시 파일 생성
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file.seek(0)  # 파일을 읽을 준비

            # 식물 영어 이름을 포함한 안전한 파일 이름 생성
            file_name = f"{plant_info.engname}.jpg"  # 영어 이름을 파일명으로 사용

            # 모델의 image 필드에 파일 저장
            plant_info.image.save(file_name, File(temp_file))

            # 서버에서 저장된 이미지의 URL을 생성 (저장된 파일의 URL 반환)
            plant_info.image_url = settings.MEDIA_URL + plant_info.image.name  # MEDIA_URL은 Django 설정에서 정의됨

            # 모델에 저장된 image_url 업데이트
            plant_info.save()
    else:
        # 이미지 다운로드 실패 시 처리
        plant_info.image_url = ""  # 빈 문자열로 실패 처리
        plant_info.save()
