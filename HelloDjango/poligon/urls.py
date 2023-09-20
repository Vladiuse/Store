from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notes', views.NoteViewSet)
router.register(r'records', views.RecordViewSet)

urlpatterns = [
    path('', views.app_root, name='poligon'),
    path('sleep_2/', views.sleep_2),
    path('', include(router.urls)),
]