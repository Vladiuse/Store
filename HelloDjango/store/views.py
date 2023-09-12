from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics, mixins, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework import permissions
from rest_framework import status

from .models import Book, Genre, Author, Comment, Favorite, Test, Like, BannerAdd
from .serializers import BookDetailSerializer, GenreSerializer, AuthorSerializer, \
    CommentSerializer, BookListSerializer, TestSerializer, LikeSerializer, BannerAddSerializer, CommentDetailSerializer
from user_api.permisions import IsOwnerPermissions, IsModeratorPermissions, IsOwnerPermissionsSafe
from shell import *
from user_api.permisions import IsEmployee, IsModeratorOrReadOnly


@api_view()
def store_root(request, format=None):
    urls = {

        'books': reverse('book-list', request=request, format=format),
        'genres': reverse('genre-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format),
        'comments': reverse('comments-list', request=request, format=format),
        'banners': reverse('banneradd-list', request=request, format=format),
    }

    if request.user.is_authenticated:
        urls.update({
            'favorite': reverse('favorite-books', request=request, format=format),
        })
    return Response(urls)


class BookListView(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Book.public.defer('description').prefetch_related('genre').select_related('author')
    serializer_class = BookListSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated, IsEmployee, IsModeratorPermissions]
        return [permission() for permission in permission_classes]


class BookDetailView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Book.public.prefetch_related('genre').prefetch_related('comment')
    serializer_class = BookDetailSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'similar_books',):
            permission_classes = []
        elif self.action == 'favorite':
            permission_classes = [permissions.IsAuthenticated, ]
        elif self.action == 'remove_from_favorite':
            permission_classes = [permissions.IsAuthenticated, IsOwnerPermissions]
        else:
            permission_classes = [permissions.IsAuthenticated, IsEmployee, IsModeratorPermissions]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Book.public. \
                prefetch_related('is_favorite'). \
                prefetch_related('genre'). \
                annotate(
                favorite=Count('is_favorite',
                               filter=Q(is_favorite__user=self.request.user)))
            return qs
        else:
            return self.queryset

    def get_object(self):
        return get_object_or_404(Book, pk=self.kwargs['pk'], is_public=True)

    @action(methods=['POST'], detail=True, )
    def favorite(self, request, pk):
        book = self.get_object()
        if book.is_favorite.filter(owner=request.user).exists():
            return Response({
                'status': 'error',
                'msg': 'Book already in favorites'
            }, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(owner=request.user, book=book)
        return Response({
            'status': 'Success',
            'msg': 'book add to favorites'
        }, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def remove_from_favorite(self, request, pk):
        book = self.get_object()
        if not book.is_favorite.filter(owner=request.user).exists():
            return Response({
                'status': 'error',
                'msg': 'Book not in favorites'
            }, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.get(owner=request.user, book=book).delete()
        return Response({
            'status': 'Success',
            'msg': 'book remove from favorites'
        }, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=True, )
    def similar_books(self, request, pk):
        book = self.get_object()
        qs = book.similar_books()
        serializer = BookListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsModeratorOrReadOnly]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    permission_classes = [IsModeratorOrReadOnly]


class CommentDetailView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerPermissionsSafe]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True,methods=['POST'],permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk):
        comment = self.get_object()
        like = comment.set_like(user=request.user)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @like.mapping.delete
    def remove_like(self, request,pk):
        comment = self.get_object()
        comment.remove_like(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,methods=['POST'],permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk):
        comment = self.get_object()
        like = comment.set_like(user=request.user)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @dislike.mapping.delete
    def remove_dislike(self, request,pk):
        comment = self.get_object()
        comment.remove_dislike(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookCommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"book": self.kwargs['book_id']})
        return context


    def list(self, request, *args, **kwargs):
        comments = self.get_queryset()
        comments_serializer = self.get_serializer(
            comments,
            many=True,
        )
        response = {
            'comments': comments_serializer.data,
        }
        if self.request.user.is_authenticated:
            user_comment = self.get_user_comment()
            user_comment_serializer = self.get_serializer(user_comment)
            response.update({
                'user_comment': user_comment_serializer.data if user_comment else None
            })
        return Response(response, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, book_id=self.kwargs['book_id'])



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, ])
def favorite_books(request, format=None):
    books = Book.objects.prefetch_related('is_favorite').filter(is_favorite__owner=request.user)
    serializer = BookDetailSerializer(books, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


class LikeViewSet(ModelViewSet):  # TODO удалить?
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, IsOwnerPermissionsSafe]
        return [permission() for permission in permission_classes]


class BannerAddViewSet(viewsets.ModelViewSet):
    serializer_class = BannerAddSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='moderator').exists():
            queryset = BannerAdd.objects.all()
        else:
            queryset = BannerAdd.public.all()
        return queryset
