from rest_framework import serializers
from .models import PlantsInfo

class PlantsInfoSerializer(serializers.ModelSerializer):
    class meta:
        model = PlantsInfo
        fields = '__all__'
        