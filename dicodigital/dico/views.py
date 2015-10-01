# -*- coding: utf-8 -*-
from rest_framework import generics, viewsets
from . import serializers, models


class Word(viewsets.ModelViewSet,
           generics.DestroyAPIView):
    queryset = models.Word.objects.all()
    serializer_class = serializers.Word


class Definition(viewsets.ModelViewSet,
                 generics.DestroyAPIView):
    queryset = models.Definition.objects.all()
    serializer_class = serializers.Definition
