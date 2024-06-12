from django.shortcuts import render, redirect
from django.http import HttpResponse
from .crawler import crawl_and_save_plant

# Create your views here.
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