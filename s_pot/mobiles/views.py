from django.http import JsonResponse
from rest_framework.decorators import api_view
from .crawler import crawl_and_save_plant

@api_view(['POST'])
def crawler_api_view(requset):
    palnt_name = requset.data.get('name')
    if not palnt_name:
        return JsonResponse({'error' : 'No plant name provided'}, staus=400)


    plant_info = crawl_and_save_plant(plant_name)
    if plant_info:
        return JsonResponse(plant_info, status=200)
    else:
        return JsonResponse({'error': 'Plant not found or failed to crawl'}, status=404)