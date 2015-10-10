# -*- coding: utf-8 -*-
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import serializers, models


class Word(viewsets.ModelViewSet, generics.CreateAPIView,
           generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = models.Word.objects.all()
    serializer_class = serializers.Word
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'

    def perform_create(self, serializer):
        """ Add the current connected user as creator """
        serializer.save(creator=self.request.user)

    def put(self, request, *args, **kwargs):
        """ Retrieve a word with its slug and update it """
        word_slug = request.data.pop('word')
        queryset = models.Word.objects.all()
        word = get_object_or_404(queryset, slug=word_slug)
        serializer = serializers.Word(
            word, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class Definition(viewsets.ModelViewSet,
                 generics.DestroyAPIView):
    queryset = models.Definition.objects.all()
    serializer_class = serializers.Definition
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
