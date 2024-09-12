from django.http import JsonResponse
from .crawler import crawl_and_save_plant
from .models import PlantsInfo
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def crawler_api(request):
    print("요청 도착")
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # 요청 바디를 JSON으로 디코딩
            print(f"Received data: {data}")

            # 데이터 형식이 리스트인 경우 처리
            if isinstance(data, list) and len(data) > 0:
                plant_name = data[0]  # 리스트의 첫 번째 요소를 가져옴
            else:
                return JsonResponse({'error': 'Invalid data format or empty list'}, status=400)

            # 가져온 데이터가 문자열인 경우 처리
            if isinstance(plant_name, str):
                result = crawl_and_save_plant(plant_name)
                if result is None:
                    return JsonResponse({'error': '해당 식물이 없습니다.'}, status=404)
                
                # 데이터베이스에서 크롤링된 식물 정보 다시 조회
                crawled_data = PlantsInfo.objects.filter(name=plant_name).values()
                data_list = list(crawled_data)
                if data_list:
                    return JsonResponse(data_list[0], safe=False, status=200)
                else:
                    return JsonResponse({'error': '해당 식물 정보를 데이터베이스에서 찾을 수 없습니다.'}, status=404)
            else:
                return JsonResponse({'error': 'Invalid plant_name format'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
