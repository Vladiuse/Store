from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Genre, MyUser

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email']
