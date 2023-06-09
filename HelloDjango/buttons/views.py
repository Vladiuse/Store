from django.http import HttpResponse
from django.shortcuts import render
from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer, JavascriptLexer, CssLexer, PhpLexer,SqlLexer
from pygments.formatters import HtmlFormatter
from .models import Button, SubButton, Language
from .serializers import ButtonSerializer, SubButtonSerializer, LanguageSerializer
style = HtmlFormatter(style='gruvbox-dark').get_style_defs('.highlight')
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view


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