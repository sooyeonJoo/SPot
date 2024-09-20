from django.http import JsonResponse
from rest_framework.decorators import api_view
from .crawler import crawl_and_save_plant
from .models import PlantsInfo

@api_view(['GET'])
def crawl_plant_info(request, plant_name):
    try:
        # 데이터베이스에서 식물 검색
        plant_info = PlantsInfo.objects.get(name=plant_name)

        # 식물 정보가 존재하면 반환
        response_data = {
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
        return JsonResponse(response_data)
