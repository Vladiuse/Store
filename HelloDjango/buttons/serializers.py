from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Genre, MyUser, Profile, Author

class BookSerializer(serializers.ModelSerializer):

    genre = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = '__all__'
        # fields = ['id', 'name', 'price', 'image', 'genre', 'author', 'available_in_store', 'is']


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


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'name']