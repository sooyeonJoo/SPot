from django.urls import path
from .views import crawler_api_view

urlpatterns = [
    path('crawler/', crawler_api_view, name='crawler_api'),
]