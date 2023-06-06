from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import UserSerializer, BookSerializer, GenreSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book, Genre


def index(request):
    return HttpResponse('GOOD!')


@api_view()
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format),
        'genres': reverse('genre-list', request=request, format=format),
    })


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
