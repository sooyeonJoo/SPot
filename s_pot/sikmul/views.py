# from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.http import JsonResponse
from .crawler import crawl_and_save_plant
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def crawler_api_view(request):
    print("요청 도착")
    if request.method == 'POST':
        try:
            print(f"Request body: {request.body}")  # 요청 본문 출력
            data = json.loads(request.body.decode('utf-8'))  # 바이너리 데이터를 문자열로 디코딩
            print(f"Received data: {data}")

            # 데이터 형식이 리스트인 경우 처리
            if isinstance(data, list) and len(data) > 0:
                plant_name = data[0]  # 리스트의 첫 번째 요소를 가져옴
            else:
                return JsonResponse({'error': 'Invalid data format or empty list'}, status=400)
            
            # 데이터 형식이 딕셔너리인 경우 처리
            if isinstance(plant_name, str):
                result = crawl_and_save_plant(plant_name)
                if result is None:
                    return JsonResponse({'error': '해당 식물이 없습니다.'}, status=404)
                
                return JsonResponse(result, status=200)
            else:
                return JsonResponse({'error': 'Invalid plant_name format'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)