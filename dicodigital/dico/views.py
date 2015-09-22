# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.filters import DjangoFilterBackend
from . import serializers, models, filters


class Word(viewsets.ModelViewSet):
    queryset = models.Word.objects.all()
    serializer_class = serializers.Word
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.Word
