from django.http import JsonResponse
from rest_framework.decorators import api_view

from .serializers import PlantsSerializer
from .crawler import crawl_and_save_plant
from .models import User, PlantsInfo,Plants
import logging

@api_view(['POST'])
def login_user(request):
    data = request.data 
    user_id = data.get('id')
    password = data.get('password')
    print(f"Received ID: {user_id}")
    print(f"Received Password: {password}")
    
    try:
        user = User.objects.get(id=user_id)
        # 평문 비밀번호 비교
        if user.passwd == password:  # 저장된 비밀번호와 입력된 비밀번호 비교
            return JsonResponse({"id": user.userid, "message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid password"}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


logger = logging.getLogger(__name__)

@api_view(['POST'])
def crawl_plant_info(request, plant_name):
    try:
        # 데이터베이스에서 식물 검색
        plant_info = PlantsInfo.objects.get(name=plant_name)

        return JsonResponse({"message": "식물 정보가 이미 존재합니다."}, status=200)

    except PlantsInfo.DoesNotExist:
        # 식물이 없으면 크롤링 진행
        plant_info = crawl_and_save_plant(plant_name)

        if plant_info is None or plant_info.get('name') == '정보 없음':
            # "정보 없음"이 이미 존재하는지 확인
            if not PlantsInfo.objects.filter(name='정보 없음').exists():
                PlantsInfo.objects.create(
                    name='정보 없음',
                    engname='정보 없음',
                    lifespan='정보 없음',
                    species='정보 없음',
                    cultivation_season='정보 없음',
                    blooming_season='정보 없음',
                    harvesting_season='정보 없음',
                    temperature='정보 없음',
                    sunlight='정보 없음',
                    watering_frequency='정보 없음',
                    pests_diseases='정보 없음'
                )
            return JsonResponse({'message': '정보 없음'}, status=404)

        # 중복 확인 후 저장
        if not PlantsInfo.objects.filter(name=plant_info.get('name')).exists():
            PlantsInfo.objects.create(
                name=plant_info.get('name'),
                engname=plant_info.get('engname'),
                lifespan=plant_info.get('lifespan'),
                species=plant_info.get('species'),
                cultivation_season=plant_info.get('cultivation_season'),
                blooming_season=plant_info.get('blooming_season'),
                harvesting_season=plant_info.get('harvesting_season'),
                temperature=plant_info.get('temperature'),
                sunlight=plant_info.get('sunlight'),
                watering_frequency=plant_info.get('watering_frequency'),
                pests_diseases=plant_info.get('pests_diseases')
            )

        return JsonResponse({"message": "식물 정보가 성공적으로 저장되었습니다."}, status=201)
    


@api_view(['GET'])   #activity_main.xml에 식물 정보 카드 띄우는 코드
def get_plants(request):
    plants = Plants.objects.all() 
    serializer = PlantsSerializer(plants, many=True)  
    return JsonResponse(serializer.data, safe=False)
    
'''
@api_view(['GET'])
def get_plants(request):
    plants = PlantsInfo.objects.all()
    serializer = PlantSerializer(plants, many=True)
    print(serializer.data)  # 로그에 데이터 출력
    return JsonResponse(serializer.data, safe=False)
'''
    
'''
교민이가 한 부분 일단 주석처리함요
@api_view(['GET'])
def crawl_plant_info(request, plant_name):
    try:
        # 데이터베이스에서 식물 검색
        plant_info = PlantsInfo.objects.get(name=plant_name)

        # 식물 정보가 존재하면 반환
        response_data = {
            'message': '성공적으로 조회되었습니다.',
            'name': plant_info.name,
            'engname': plant_info.engname,
            'lifespan': plant_info.lifespan,
            'species': plant_info.species,
            'cultivation_season': plant_info.cultivation_season,
            'blooming_season': plant_info.blooming_season,
            'harvesting_season': plant_info.harvesting_season,
            'temperature': plant_info.temperature,
            'sunlight': plant_info.sunlight,
            'watering_frequency': plant_info.watering_frequency,
            'pests_diseases': plant_info.pests_diseases
        }
        return JsonResponse(response_data)

    except PlantsInfo.DoesNotExist:
        # 식물이 없으면 크롤링 진행
        plant_info = crawl_and_save_plant(plant_name)

        if plant_info is None or plant_info.get('name') == '정보 없음':
            # "정보 없음"이 이미 존재하는지 확인
            if not PlantsInfo.objects.filter(name='정보 없음').exists():
                PlantsInfo.objects.create(
                    name='정보 없음',
                    engname='정보 없음',
                    lifespan='정보 없음',
                    species='정보 없음',
                    cultivation_season='정보 없음',
                    blooming_season='정보 없음',
                    harvesting_season='정보 없음',
                    temperature='정보 없음',
                    sunlight='정보 없음',
                    watering_frequency='정보 없음',
                    pests_diseases='정보 없음'
                )
            return JsonResponse({'message': '정보 없음'}, status=404)

        # 중복 확인 후 저장
        if not PlantsInfo.objects.filter(name=plant_info.get('name')).exists():
            PlantsInfo.objects.create(
                name=plant_info.get('name'),
                engname=plant_info.get('engname'),
                lifespan=plant_info.get('lifespan'),
                species=plant_info.get('species'),
                cultivation_season=plant_info.get('cultivation_season'),
                blooming_season=plant_info.get('blooming_season'),
                harvesting_season=plant_info.get('harvesting_season'),
                temperature=plant_info.get('temperature'),
                sunlight=plant_info.get('sunlight'),
                watering_frequency=plant_info.get('watering_frequency'),
                pests_diseases=plant_info.get('pests_diseases')
            )

        response_data = {
            'message': '성공적으로 크롤링되었습니다.',
            'name': plant_info.get('name'),
            'engname': plant_info.get('engname'),
            'lifespan': plant_info.get('lifespan'),
            'species': plant_info.get('species'),
            'cultivation_season': plant_info.get('cultivation_season'),
            'blooming_season': plant_info.get('blooming_season'),
            'harvesting_season': plant_info.get('harvesting_season'),
            'temperature': plant_info.get('temperature'),
            'sunlight': plant_info.get('sunlight'),
            'watering_frequency': plant_info.get('watering_frequency'),
            'pests_diseases': plant_info.get('pests_diseases')
        }
        return JsonResponse(response_data, status=200)
'''