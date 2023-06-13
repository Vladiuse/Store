from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'genres',views.GenreViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'comments', views.CommentViewSet)

# router.register(r'books/<int:pk>/comments/', views.CommentViewSet, basename='book-comments')

router.register(r'books',views.BookListView)
router.register(r'books',views.BookDetailView)

comments_list = views.BookCommentViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('', views.api_root, name='store'),
    path('favorite/', views.favorite_books, name='favorite'),
    path('books/<int:book_id>/comments/',comments_list, name='book-comment-list'),
    path('', include(router.urls)),
]