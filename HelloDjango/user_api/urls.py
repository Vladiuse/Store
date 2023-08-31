from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'users-addresses', views.UserAddressViewSet)

urlpatterns = [
    path('', views.api_root, name='auth_root'),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('user', views.UserView.as_view(), name='user'),
    path('', include(router.urls)),
]