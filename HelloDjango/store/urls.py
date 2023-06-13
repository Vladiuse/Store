from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'genres',views.GenreViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'comments', views.CommentViewSet)

router.register(r'books',views.BookListView)
router.register(r'books',views.BookDetailView)

urlpatterns = [
    path('', views.api_root, name='store'),
    path('favorite/', views.favorite_books, name='favorite'),
    path('', include(router.urls)),
]