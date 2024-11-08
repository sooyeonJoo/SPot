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

class PlantsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantsInfo
        fields = ['temperature']  # temperature 필드만 포함

class PlantsSerializer(serializers.ModelSerializer):
    name = PlantsInfoSerializer()  # 연결된 PlantsInfo의 temperature 필드를 포함

    class Meta:
        model = Plants
        fields = ['plantsid', 'userid', 'name', 'nickname', 'birthday', 'deathday', 'color', 'wateringInterval']


class PlantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plants
        fields = ['nickname', 'birthday','color','wateringInterval']

class WateringscheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wateringschedule
        fields = ['date']


