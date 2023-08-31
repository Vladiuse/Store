from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import MyUser, Profile, UserAddress

User = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):  # TODO проверка пароля - короткий нельзя
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


class ProfileAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    # TODO make owner be username not pk
    url = serializers.HyperlinkedIdentityField(view_name='profile-detail')

    class Meta:
        model = Profile
        fields = ['owner', 'first_name', 'last_name', 'age', 'sex', 'url', ]
        extra_kwargs = {
            'owner': {'read_only': True}
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # addresses = ProfileAddressSerializer(many=True, read_only=True) TODO add maybe

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'is_staff', 'date_joined', 'url']


class UserAddressSerializer(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['pk', 'owner', 'address']
        extra_kwargs = {
            'owner': {'read_only': True, },
        }
