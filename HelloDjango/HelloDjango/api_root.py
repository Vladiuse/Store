from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view()
def index(request, format=None):
    return Response({
    'apps':{
        'buttons_app': reverse('buttons_root', request=request, format=format),
        'store_app': reverse('store', request=request, format=format),
        'poligon_app': reverse('poligon', request=request, format=format),
        'user_api': reverse('auth_root', request=request, format=format),
    },
    'docs':{
        'swagger': reverse('schema-swagger-ui', request=request, format=format),
        'redoc': reverse('schema-redoc', request=request, format=format),
    }
})

