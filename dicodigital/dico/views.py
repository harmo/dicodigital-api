# -*- coding: utf-8 -*-
from rest_framework import generics, viewsets, permissions
from . import serializers, models


class Word(viewsets.ModelViewSet,
           generics.DestroyAPIView):
    queryset = models.Word.objects.all()
    serializer_class = serializers.Word
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """ Add the current connected user as creator """
        serializer.save(creator=self.request.user)


class Definition(viewsets.ModelViewSet,
                 generics.DestroyAPIView):
    queryset = models.Definition.objects.all()
    serializer_class = serializers.Definition
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
