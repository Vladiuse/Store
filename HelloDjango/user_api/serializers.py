from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers


UserModel = get_user_model()

class UserRegistrationSerializer(ModelSerializer):

    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ['username', 'password']

    def check_user(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        if user:
            return user
        else:
            print(validated_data)
            raise ValueError

class UserSerializer(ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['username', 'email']