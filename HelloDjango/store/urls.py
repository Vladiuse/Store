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

comments_detail = views.CommentDetailView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
})

urlpatterns = [
    path('', views.store_root, name='store'),
    path('favorite/', views.favorite_books, name='favorite-books'),
    path('books/<int:book_id>/comments/', views.BookCommentListView.as_view(), name='book-comment-list'),
    path('comments/<int:pk>/', comments_detail, name='comment-detail'),
    path('comments/<int:pk>/like/', comments_detail, name='comment-like'),
    path('comments/<int:pk>/dislike/', comments_detail, name='comment-dislike'),
    path('', include(router.urls)),
]