from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics, mixins, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status

from .models import Book, Genre, Author, Comment, Favorite, Test, Like
from .serializers import BookDetailSerializer, GenreSerializer, UserSerializer, AuthorSerializer, \
    CommentSerializer, BookListSerializer, ProfileSerializer, TestSerializer, LikeSerializer
from .permisions import IsOwnerPermissions, IsModeratorPermissions
from user_api.models import MyUser, Profile
from django.conf import settings




@api_view()
def store_root(request, format=None):
    urls = {

        'books': reverse('book-list', request=request, format=format),
        'genres': reverse('genre-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format),
        'comments': reverse('comments-list', request=request, format=format),
        '__TEST__': reverse('test-list', request=request, format=format),
    }

    if request.user.is_authenticated:
        urls.update({
            'users': reverse('myuser-list', request=request, format=format),
            'profiles': reverse('profile-list', request=request, format=format),
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


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermissions,]

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')



class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    @action(methods=['POST', 'GET'], detail=True, permission_classes=[permissions.IsAuthenticated, ])
    def like(self,request, pk):
        comment = self.get_object()
        comment.set_like(user=request.user)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    @action(methods=['POST', 'GET'], detail=True, permission_classes=[permissions.IsAuthenticated, ])
    def dislike(self,request, pk):
        comment = self.get_object()
        comment.set_dislike(user=request.user)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)



class BookCommentViewSet(mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        qs = Comment.objects.filter(book_id=self.kwargs['book_id']).select_related('owner').select_related('book')
        if self.request.user.is_authenticated:
            qs = qs.exclude(owner=self.request.user)
        return qs

    def get_user_comment(self):
        try:
            user_comment = Comment.objects.get(book_id=self.kwargs['book_id'], owner=self.request.user)
        except Comment.DoesNotExist:
            user_comment = None
        return user_comment

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerPermissions]
        if self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, IsOwnerPermissions | IsModeratorPermissions]
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
        serializer = CommentSerializer(data=data, context={'request', self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, book_id= self.kwargs['book_id'])
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, owner=request.user, book=self.kwargs['book_id'])
        self.check_object_permissions(request, comment)
        partial = kwargs.pop('partial', False)
        data = request.data
        data.update({
            'owner': request.user.pk,
            'book': self.kwargs['book_id'],
        })
        serializer = CommentSerializer(comment, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwarg):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, ])
def favorite_books(request, format=None):
    books = Book.objects.prefetch_related('is_favorite').filter(is_favorite__user=request.user)
    serializer = BookDetailSerializer(books, many=True)
    return Response(serializer.data)


def test(request, pk):
    return Response({})


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, IsModeratorPermissions]
            return [permission() for permission in permission_classes]
        return [permission() for permission in permission_classes]
