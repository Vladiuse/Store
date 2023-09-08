from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'genres',views.GenreViewSet)
router.register(r'authors', views.AuthorViewSet)

# router.register(r'comments', views.CommentView, basename='comments')
router.register(r'likes', views.LikeViewSet)
router.register(r'banners', views.BannerAddViewSet)


router.register(r'books',views.BookListView)
router.register(r'books',views.BookDetailView)

# comments_list = views.BookCommentViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
#     'put': 'update',
#     'patch': 'partial_update',
# })
comments_detail = views.CommentView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
})

urlpatterns = [
    path('', views.store_root, name='store'),
    path('favorite/', views.favorite_books, name='favorite'),
    path('books/<int:book_id>/comments/', views.BookCommentListView.as_view(), name='book-comment-list'),
    path('comments/<int:pk>/', comments_detail, name='comment-detail'),
    path('comments/<int:pk>/like/', comments_detail, name='comment-like'),
    path('comments/<int:pk>/dislike/', comments_detail, name='comment-dislike'),
    path('', include(router.urls)),
]