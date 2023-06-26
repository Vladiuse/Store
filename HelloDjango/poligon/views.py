from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet
from .models import Record, Note
from .serializers import NoteSerializer, RecordSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

@api_view()
def app_root(request, format=None):
    return Response({
        'notes': reverse('note-list', request=request, format=format),
        'records(need auth)': reverse('record-list', request=request, format=format),
    })


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class RecordViewSet(ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated,]