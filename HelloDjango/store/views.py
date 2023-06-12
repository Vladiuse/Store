from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import BookSerializer, GenreSerializer, UserSerializer, AuthorSerializer, \
    CommentSerializer, BookListSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .models import Book, Genre, MyUser, Author, Comment, Favorite
from rest_framework import permissions
from django.db.models import Count, Q


@api_view()
def api_root(request, format=None):
    return Response({
        'users': reverse('myuser-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format),
        'genres': reverse('genre-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format),
    })


class BookViewSet(ModelViewSet):
    queryset = Book.objects.prefetch_related('genre')
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Book.objects.\
                prefetch_related('is_favorite'). \
                prefetch_related('genre').\
                annotate(
                favorite=Count('is_favorite',
                filter=Q(is_favorite__user=self.request.user)))
            return qs
        else:
            return self.queryset

    @action(detail=True, methods=['patch',], permission_classes=[permissions.IsAuthenticated,])
    def favorite(self, request, pk):
        book = self.get_object()
        if book.is_favorite.filter(user=request.user).exists():
            raise ZeroDivisionError
        Favorite.objects.create(user=request.user, book=book)
        return Response({
            'status':'Success',
            'msg': 'book add to favorites'
        })

    @favorite.mapping.delete
    def remove_from_favorite(self, request,pk):
        book = self.get_object()
        if not book.is_favorite.filter(user=request.user).exists():
            raise ZeroDivisionError
        Favorite.objects.get(user=request.user, book=book).delete()
        return Response({
            'status':'Success',
            'msg': 'book remove from favorites'
        })








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


class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
