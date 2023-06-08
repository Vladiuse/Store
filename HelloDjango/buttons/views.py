from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import  BookSerializer, GenreSerializer, UserSerializer, AuthorSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book, Genre, MyUser, Author
from rest_framework import permissions

@api_view()
def index(request, format=None):
    return Response({
        'api_root': reverse('api_root', request=request, format=format),
        'swagger': reverse('schema-swagger-ui', request=request, format=format),
        'redoc': reverse('schema-redoc', request=request, format=format)
    })


@api_view()
def api_root(request, format=None):
    return Response({
        'users': reverse('myuser-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format),
        'genres': reverse('genre-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format),
    })


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

