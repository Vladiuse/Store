from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, ProfileSerializer, \
    UserAddressSerializer
from rest_framework.response import Response
from rest_framework import authentication
from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from .models import MyUser, Profile, UserAddress
from .permisions import IsOwnerPermissions, IsEmployee
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import mixins


@api_view()
def api_root(request, format=None):
    urls = {
        'register': reverse('register', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'logout': reverse('logout', request=request, format=format),
        'user': reverse('user', request=request, format=format),
    }

    if request.user.is_authenticated:
        urls.update({
            'users': reverse('myuser-list', request=request, format=format),
            'profiles': reverse('profile-list', request=request, format=format),
            'favorite': reverse('favorite-books', request=request, format=format),
        })
    return Response(urls)


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'user': serializer.data
        })


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.SessionAuthentication, ]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.check_user(request.data)
        login(request, user)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class UserLogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.SessionAuthentication,authentication.BasicAuthentication)

    ##
    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet
                  ):
    queryset = MyUser.objects.select_related('profile').all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsEmployee)


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            permission_classes = [permissions.IsAuthenticated, IsOwnerPermissions]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerPermissions | IsEmployee]
        return [permission() for permission in permission_classes]


class UserAddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, IsOwnerPermissions | IsEmployee]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [permissions.IsAuthenticated, IsOwnerPermissions]
        else:  # list
            permission_classes = [permissions.IsAuthenticated, IsEmployee]
        return [permission() for permission in permission_classes]