from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view



def index(request):
    return HttpResponse('GOOD!')

@api_view()
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format)
    })


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


