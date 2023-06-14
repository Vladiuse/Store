from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import BookDetailSerializer, GenreSerializer, UserSerializer, AuthorSerializer, \
    CommentSerializer, BookListSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes
from .models import Book, Genre, MyUser, Author, Comment, Favorite
from rest_framework import permissions
from django.db.models import Count, Q
from rest_framework import generics, mixins, viewsets
from rest_framework.viewsets import GenericViewSet


@api_view()
def store_root(request, format=None):
    urls = {
        'users': reverse('myuser-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format),
        'genres': reverse('genre-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format),
    }

    if request.user.is_authenticated:
        urls.update({
            'favorite': reverse('favorite', request=request, format=format),
        })
    return Response(urls)


class BookListView(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Book.objects.prefetch_related('genre')
    serializer_class = BookListSerializer


class BookDetailView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Book.objects.prefetch_related('genre').prefetch_related('comment')
    serializer_class = BookDetailSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Book.objects. \
                prefetch_related('is_favorite'). \
                prefetch_related('genre'). \
                annotate(
                favorite=Count('is_favorite',
                               filter=Q(is_favorite__user=self.request.user)))
            return qs
        else:
            return self.queryset

    @action(methods=['PATCH'], detail=True, permission_classes=[permissions.IsAuthenticated, ])
    def favorite(self, request, pk):
        book = self.get_object()
        if book.is_favorite.filter(user=request.user).exists():
            return Response({
                'status': 'error',
                'msg': 'Book already in favorites'
            })
        Favorite.objects.create(user=request.user, book=book)
        return Response({
            'status': 'Success',
            'msg': 'book add to favorites'
        })

    @favorite.mapping.delete
    def remove_from_favorite(self, request, pk):
        book = self.get_object()
        if not book.is_favorite.filter(user=request.user).exists():
            return Response({
                'status': 'error',
                'msg': 'Book not in favorites'
            })
        Favorite.objects.get(user=request.user, book=book).delete()
        return Response({
            'status': 'Success',
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


class BookCommentViewSet(viewsets.GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        qs = Comment.objects.filter(book_id=self.kwargs['book_id']).select_related('user').select_related('book')
        if self.request.user.is_authenticated:
            qs = qs.exclude(user=self.request.user)
        return qs

    def get_user_comment(self):
        try:
            user_comment = Comment.objects.get(book_id=self.kwargs['book_id'], user=self.request.user)
        except Comment.DoesNotExist:
            user_comment = None
        return user_comment

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        comments = self.get_queryset()
        comments_serializer = self.get_serializer(comments, many=True)
        response = {
            'comments': comments_serializer.data,
        }
        if self.request.user.is_authenticated:
            user_comment_serializer = self.get_serializer(self.get_user_comment())
            response.update({
                'user_comment': user_comment_serializer.data
            })
        return Response(response)

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({
            'user': request.user.pk,
            'book': self.kwargs['book_id'],
        })
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, ])
def favorite_books(request, format=None):
    books = Book.objects.prefetch_related('is_favorite').filter(is_favorite__user=request.user)
    serializer = BookDetailSerializer(books, many=True)
    return Response(serializer.data)


def test(request, pk):
    return Response({})
