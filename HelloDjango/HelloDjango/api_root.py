from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view()
def index(request, format=None):
    return Response({
        'buttons': reverse('buttons_root', request=request, format=format),
        'store': reverse('store', request=request, format=format),
        'swagger': reverse('schema-swagger-ui', request=request, format=format),
        'redoc': reverse('schema-redoc', request=request, format=format),
    })