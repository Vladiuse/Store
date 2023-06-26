from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.api_root, name='auth_root'),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('user', views.UserView.as_view(), name='user'),
]