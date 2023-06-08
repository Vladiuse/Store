from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Genre, MyUser, Profile

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'age']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email','is_staff', 'profile', 'date_joined']

