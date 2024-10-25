from rest_framework import serializers
from .models import User, PlantsInfo, Plants

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class PlantsInfoSerializer(serializers.ModelSerializer):
    class meta:
        model = PlantsInfo
        fields = '__all__'
        

class PlantsSerializer(serializers.ModelSerializer):
    class meta:
        model = Plants
        fields = ['nickname', 'birthday', 'deathday','color','wateringInterval']