from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books',views.BookViewSet)
router.register(r'genres',views.GenreViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api_root, name='api_root'),
    path('api/', include(router.urls)),
]