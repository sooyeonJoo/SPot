# from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.http import JsonResponse
from .crawler import crawl_and_save_plant
import json

# Create your views here.
'''
def sikmul(request):
  return HttpResponse("Hello")

def crawling_view(request):
    if request.method == 'POST':
        plant_name = request.POST.get('plant_name')
        if not plant_name:
            return render(request, 'crawling_form.html', {'error': '식물 이름을 입력하세요'})

        result = crawl_and_save_plant(plant_name)
        if result is None:
            return render(request, 'crawling_form.html', {'error': '해당 식물이 없습니다.'})
        return redirect('success')
    return render(request, 'crawling_form.html')

def success_view(request):
    return render(request, 'success.html')
'''

def crawler_api_view(request):
    print("요청 도착")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plant_name = data.get('plant_name')
            if not plant_name:
                return JsonResponse({'error': '식물 이름을 입력하세요'}, status=400)

            result = crawl_and_save_plant(plant_name)
            if result is None:
                return JsonResponse({'error': '해당 식물이 없습니다.'}, status=404)
            
            return JsonResponse(result, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method(잘못된 HTTP 메소드)'}, status=405)