from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'languages', views.LanguageViewSet)
router.register(r'buttons', views.ButtonViewSet)
router.register(r'sub_buttons', views.SubButtonViewSet)


urlpatterns = [
    path('test/', views.test,name='test'),
    path('', views.buttons_api_root, name='buttons_root'),
    path('', include(router.urls),),
    path('buttons/<int:button_id>/subs/', views.sub_buttons, name='subs_buttons'),
]