from rest_framework import serializers
from .models import User, PlantsInfo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class PlantsInfoSerializer(serializers.ModelSerializer):
    class meta:
        model = PlantsInfo
        fields = '__all__'
        