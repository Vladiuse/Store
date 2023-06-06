from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff']


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
