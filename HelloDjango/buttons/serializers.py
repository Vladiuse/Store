from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Genre, MyUser, Profile

class BookSerializer(serializers.ModelSerializer):

    genre = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'image', 'genre']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'sex']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email','is_staff', 'profile', 'date_joined']

