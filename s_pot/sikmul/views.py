from django.shortcuts import render, redirect
from django.http import HttpResponse
from .crawler import crawl_and_save_plant
from .models import PlantsInfo

# Create your views here.
def sikmul(request):
  return HttpResponse("Hello")

def crawling_view(request):
    if request.method == 'POST':
        plant_name = request.POST.get('plant_name')
        if not plant_name:
            return render(request, 'crawling_form.html', {'error': '식물 이름을 입력하세요'})

        # 데이터베이스에서 식물 이름 확인
        existing_plant = PlantsInfo.objects.filter(name=plant_name).first()
        if existing_plant:
            # 데이터가 있는 경우 템플릿에 데이터를 전달하여 렌더링
            return render(request, 'plant_detail.html', {'plant': existing_plant})

        # 크롤링 및 저장
        result = crawl_and_save_plant(plant_name)
        if result is None:
            return render(request, 'crawling_form.html', {'error': '해당 식물이 없습니다.'})
        return redirect('success')
    return render(request, 'crawling_form.html')

def success_view(request):
    return render(request, 'success.html')

def success_view(request):
    return render(request, 'success.html')