from django.http import HttpResponse
from rest_framework import generics
from django.http import HttpResponse
from django.shortcuts import render
from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer, JavascriptLexer, CssLexer, PhpLexer,SqlLexer
from pygments.formatters import HtmlFormatter
from .models import Button, SubButton, Language, X
from .serializers import ButtonSerializer, SubButtonSerializer, LanguageSerializer, XSerializer
style = HtmlFormatter(style='gruvbox-dark').get_style_defs('.highlight')
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
import django_filters.rest_framework
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.settings import api_settings


def test(request):
    buttons = Button.objects.all()
    content = {
        'buttons': buttons,
        'style':style,
    }
    return render(request, 'buttons/test.html', content)


@api_view()
def buttons_api_root(request, format=None):
    return Response({
        'languages': reverse('language-list', request=request, format=format),
        'buttons': reverse('button-list', request=request, format=format),
        'sub_buttons': reverse('subbutton-list', request=request, format=format),
        'test': reverse('test', request=request, format=format),
    })


@api_view()
def sub_buttons(request, button_id, format=None):
    button = Button.objects.get(pk=button_id)
    subs = SubButton.objects.filter(parent=button)
    serializer = SubButtonSerializer(subs, many=True)
    return Response({'subs':serializer.data})

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ButtonViewSet(viewsets.ModelViewSet):
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer


class SubButtonViewSet(viewsets.ModelViewSet):
    queryset = SubButton.objects.all()
    serializer_class = SubButtonSerializer

    def get_view_description(self):
        return 'ABCDEF'

@api_view()
def filter(request):
    res =  Response({'value': 'xxx'})
    res.data['yyy'] = 'yyy'
    return res


def show(qs,**kwargs):
    print(kwargs)
    for k, v in kwargs.items():
        print(k,v, type(v), qs[k])


class MyPaginator(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'ppage'


class XView(generics.ListAPIView):
    serializer_class = XSerializer
    queryset = X.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['x', 'y']
    search_fields = ['x', 'y']
    ordering_fields = ['pk', 'x']
    pagination_class = CursorPagination
    ordering = ['-pk']

    # def get_queryset(self):
    #     print(self.request.query_params)
    #     return X.objects.filter(x=self.request.query_params['x'])
    # def get(self, request, *args, **kwargs):
    #     qs = self.get_queryset()
    #     serializer = self.get_serializer(qs, many=True)
    #     return Response({
    #         'var': self.kwargs['xxx'],
    #         'params': self.request.query_params,
    #         'items': serializer.data,
    #
    #     })