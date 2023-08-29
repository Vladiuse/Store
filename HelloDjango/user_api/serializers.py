from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class UserRegistrationSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
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
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(
            username=username,
            password=password,
        )
        if user:
            return user
        else:
            raise AuthenticationFailed(detail='Incorrect username or password')

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']