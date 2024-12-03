from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .crawler import crawl_and_save_plant
from .models import User, PlantsInfo, Plants, Wateringschedule
import logging
from .serializers import UserSerializer, PlantsSerializer
from rest_framework import status
from schedules.waterdbmanage import save_watering_data_and_schedule_update  # waterdbmanager에서 함수 import
from django.utils import timezone

@api_view(['POST'])
def login_user(request):
    data = request.data 
    user_id = data.get('id')
    password = data.get('passwd')
    
    try:
        user = User.objects.get(id=user_id)
        # 평문 비밀번호 비교
        if user.passwd == password:
            return JsonResponse({"id": user.userid, "name": user.name, "message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid password"}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

logger = logging.getLogger(__name__)


@api_view(['POST'])
def join_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # 유효하면 User 모델에 저장
        return JsonResponse({"id": serializer.data.get('id'), "message": "Join successful"})
    else:
        return Response(serializer.errors, status=400)


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


@api_view(['GET'])   #식물카드 띄우는 부분
def get_plants(request):
    plants = Plants.objects.all() 
    serializer = PlantsSerializer(plants, many=True)  
    return JsonResponse(serializer.data, safe=False)
    

@api_view(['POST'])
def send_plant_data(request):
    if request.method == 'POST':
        nickname = request.data.get('nickname')
        birth_date = request.data.get('birthDate')
        color = request.data.get('color')
        watering_days = request.data.get('wateringDays')
        plant_name = request.data.get('name')
        user_id = 1
        

        # 유효성 검사
        if not nickname or not birth_date or not color or not watering_days or not plant_name:
            return Response({'error': '모든 필드를 올바르게 입력해 주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # PlantsInfo를 찾기
        plant_info = PlantsInfo.objects.filter(name=plant_name).first()
        if not plant_info:
            return Response({'error': '식물 정보가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        

        # 새로운 식물 등록
        plant = Plants.objects.create(
            name=plant_info,  # 외래키 연결
            userid_id=user_id,
            nickname=nickname,
            birthday=birth_date,
            color=color,
            wateringInterval=watering_days
        )

        return Response({'success': True, 'plantId': plant.plantsid}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def send_watering_schedule(request):
    if request.method == 'POST':
        start_date = request.data.get('startDate')
        plants_id = request.data.get('plantId')
        user_id = 2  # 하드코딩된 사용자 ID

        # 유효성 검사
        if not start_date or not plants_id:
            return Response({'error': '모든 필드를 입력해 주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # `start_date` 변환
        try:
            start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': '유효하지 않은 날짜 형식입니다. (YYYY-MM-DD)'}, status=status.HTTP_400_BAD_REQUEST)

        # `plantsid` 확인
        plant = Plants.objects.get(plantsid=plants_id)
        if not plant:
            return Response({'error': '식물 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 기존 물 주기 값 가져오기 (기존 wateringInterval 값 사용)
        #watering_interval = plant.wateringInterval

        # 일정 저장 함수 호출
        try:
            save_watering_data_and_schedule_update(plant.plantsid, start_date)
        except Exception as e:
            return Response({'error': f'일정 생성 중 오류 발생: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True, 'message': '일정이 성공적으로 생성되었습니다.'}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def get_watering_frequency(request, plant_name):
    # plant_name을 기준으로 PlantsInfo 테이블에서 조회
    plant_info = PlantsInfo.objects.filter(name=plant_name).first()

    if not plant_info:
        return Response({'error': '식물 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 물 공급 주기 가져오기
    watering_frequency = plant_info.watering_frequency  # PlantsInfo에서 가져옴
    return Response({'wateringFrequency': watering_frequency, 'success': True}, status=status.HTTP_200_OK)


#activity_info.xml에식물 정보 불러오는거
def get_plant_info(request):
    plant_name = request.GET.get('plantName', None)  # 쿼리 파라미터에서 plantName 가져오기
    
    if plant_name:
        try:
            # PlantsInfo 모델에서 plant_name을 기반으로 정보 조회
            plant = PlantsInfo.objects.get(name=plant_name)
            
            # 반환할 필드들을 name을 제외하고 작성
            response_data = {
                'engname': plant.engname,
                'lifespan': plant.lifespan,
                'species': plant.species,
                'cultivation_season': plant.cultivation_season,
                'blooming_season': plant.blooming_season,
                'harvesting_season': plant.harvesting_season,
                'sunlight': plant.sunlight,
                'watering_frequency': plant.watering_frequency,
                'temperature': plant.temperature,
                'pests_diseases': plant.pests_diseases,
            }
            return JsonResponse(response_data)
        except PlantsInfo.DoesNotExist:
            return JsonResponse({'error': 'Plant not found'}, status=404)
    else:
        return JsonResponse({'error': 'Plant name is required'}, status=400)    
    


