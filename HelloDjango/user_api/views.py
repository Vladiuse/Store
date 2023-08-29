from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import authentication
from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

@api_view()
def api_root(request, format=None):
    return Response({
        'register': reverse('register', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'logout': reverse('logout', request=request, format=format),
        'user': reverse('user', request=request, format=format),
    })

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': serializer.data
        })

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.SessionAuthentication,]


    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.check_user(request.data)
        login(request,user)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserLogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)



class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.SessionAuthentication,)
    ##
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)