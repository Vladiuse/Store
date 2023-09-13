from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'genres',views.GenreViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'likes', views.LikeViewSet)
router.register(r'banners', views.BannerAddViewSet, basename='banners')
router.register(r'books',views.BookListView)
router.register(r'books',views.BookDetailView)
router.register(r'comments', views.CommentDetailView)
router.register(r'basket', views.BasketViewSet, basename='basket')


urlpatterns = [
    path('', views.store_root, name='store'),
    path('favorite/', views.favorite_books, name='favorite-books'),
    path('books/<int:book_id>/comments/', views.BookCommentListView.as_view(), name='book-comment-list'),
    path('', include(router.urls)),
]