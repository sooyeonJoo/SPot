from rest_framework import serializers
from .models import User, PlantsInfo, Plants,Wateringschedule

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class PlantsInfoSerializer(serializers.ModelSerializer):
    class meta:
        model = PlantsInfo
        fields = '__all__'

class PlantsInfoPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantsInfo
        fields = ['name','temperature'] #식물 이름과 온도를  포함

class PlantsSerializer(serializers.ModelSerializer):
    plant_info = PlantsInfoSerializer()
    name = PlantsInfoPartSerializer()  # 연결된 PlantsInfo의 temperature 필드를 포함

    class Meta:
        model = Plants
        fields = ['plantsid', 'userid', 'name', 'nickname', 'birthday', 'deathday', 'color', 'wateringInterval']
        read_only_fields = ['name'] 

class WateringscheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wateringschedule
        fields = ['date']


