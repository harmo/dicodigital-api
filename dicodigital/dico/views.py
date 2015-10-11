# -*- coding: utf-8 -*-
from rest_framework import generics, viewsets, permissions, status, pagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import serializers, models


class WordCursorPagination(pagination.CursorPagination):
    ordering = 'slug'
    page_size = 20


class DefinitionCursorPagination(pagination.CursorPagination):
    ordering = 'word_id'
    page_size = 20


class Word(viewsets.ModelViewSet, generics.CreateAPIView,
           generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = models.Word.objects.all()
    serializer_class = serializers.Word
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    pagination_class = WordCursorPagination

    def get_queryset(self):
        return models.Word.objects\
            .prefetch_related('creator', 'definitions__contributor')\
            .all()

    def perform_create(self, serializer):
        """ Add the current connected user as creator """
        serializer.save(creator=self.request.user)

    def put(self, request, *args, **kwargs):
        """ Retrieve a word with its slug and update it """
        if 'word' not in request.data:
            return Response('word parameter is missing',
                            status=status.HTTP_400_BAD_REQUEST)

        word_slug = request.data.pop('word')
        queryset = models.Word.objects.all()
        word = get_object_or_404(queryset, slug=word_slug)
        serializer = serializers.Word(
            word, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class Definition(viewsets.ModelViewSet, generics.CreateAPIView,
                 generics.DestroyAPIView):
    queryset = models.Definition.objects.all()
    serializer_class = serializers.Definition
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = DefinitionCursorPagination

    def get_queryset(self):
        return models.Definition.objects\
            .prefetch_related('contributor', 'word')\
            .all()

    def perform_create(self, serializer):
        """ Add the current connected user as contributor """
        serializer.save(contributor=self.request.user,
                        word=self.request.data['word'])

    def create(self, request, *args, **kwargs):
        """ Check if word parameter is in data """
        if 'word' not in self.request.data:
            return Response('word parameter is missing',
                            status=status.HTTP_400_BAD_REQUEST)
        return super(Definition, self).create(request, *args, **kwargs)
