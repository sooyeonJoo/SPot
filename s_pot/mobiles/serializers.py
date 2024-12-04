from rest_framework import serializers
from .models import User, PlantsInfo, Plants, Wateringcalendar, Wateringschedule

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'passwd', 'name', 'birthday', 'gender', 'tel', 'email']
        extra_kwargs = {
            'birthday': {'required': False},
            'gender': {'required': False},
            'tel': {'required': False},
            'email': {'required': False}
        }

class PlantsInfoSerializer(serializers.ModelSerializer):
    class meta:
        model = PlantsInfo
        fields = '__all__'


class PlantsInfoPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantsInfo
        fields = ['name','temperature','image_url'] 


class PlantsSerializer(serializers.ModelSerializer):
    name = PlantsInfoPartSerializer() #연결된 PlantsInfo에서 name과 temperature 가져오기
    class Meta:
        model = Plants
        fields = ['plantsid','nickname','name', 'birthday', 'color', 'wateringInterval' ]

class WateringcalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wateringcalendar
        fields = ['date']

class WateringscheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wateringschedule
        fields = ['date']
