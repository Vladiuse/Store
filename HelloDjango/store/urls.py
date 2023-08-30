from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'genres',views.GenreViewSet)
# router.register(r'users', views.UserViewSet)
# router.register(r'profiles', views.ProfileViewSet)
router.register(r'authors', views.AuthorViewSet)

router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'likes', views.LikeViewSet)
router.register(r'banners', views.BannerAddViewSet)


router.register(r'books',views.BookListView)
router.register(r'books',views.BookDetailView)

comments_list = views.BookCommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'patch': 'partial_update',
})
comments_detail = views.BookCommentViewSet.as_view({
    'delete': 'destroy',
})

urlpatterns = [
    path('', views.store_root, name='store'),
    path('favorite/', views.favorite_books, name='favorite'),
    path('books/<int:book_id>/comments/',comments_list, name='book-comment-list'),
    path('books/<int:book_id>/comments/<int:pk>/', comments_detail, name='book-comment-detail'),
    path('', include(router.urls)),
]