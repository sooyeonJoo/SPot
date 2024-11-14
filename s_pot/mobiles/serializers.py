from rest_framework import serializers
from .models import User, PlantsInfo, Plants,Wateringschedule

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'passwd', 'name', 'birthday', 'gender', 'tel', 'email']

class PlantsInfoSerializer(serializers.ModelSerializer):
    class meta:
        model = PlantsInfo
        fields = '__all__'

class PlantsInfoPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantsInfo
        fields = ['name','temperature'] #식물 이름과 온도를  포함

class PlantsSerializer(serializers.ModelSerializer):
    name = PlantsInfoPartSerializer() #연결된 PlantsInfo에서 name과 temperature 가져오기
    class Meta:
        model = Plants
        fields = ['nickname','name', 'birthday', 'color', 'wateringInterval' ]

class WateringscheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wateringschedule
        fields = ['date']


