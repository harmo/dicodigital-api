# -*- coding: utf-8 -*-
from rest_framework import generics, viewsets, permissions, status, pagination, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import serializers, models


class WordCursorPagination(pagination.CursorPagination):
    ordering = 'label'
    page_size = 20


class DefinitionCursorPagination(pagination.CursorPagination):
    ordering = 'word_id'
    page_size = 20


class Checks(object):

    class Meta:
        abstract = True

    def check_word_id(self):
        """ Check if word parameter is in data """
        if 'word' not in self.request.data:
            return 'Word parameter is missing'
        """ Check if word parameter is not None """
        if self.request.data['word'] is None:
            return 'Word ID cannot be None'
        """ Check if word parameter is > 0 """
        if self.request.data['word'] < 1:
            return 'Word ID must be an integer > 0'


class Word(viewsets.ModelViewSet, generics.CreateAPIView,
           generics.UpdateAPIView, generics.DestroyAPIView, Checks):
    queryset = models.Word.objects.all()
    serializer_class = serializers.Word
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    pagination_class = WordCursorPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('label',)

    def get_queryset(self):
        return super(Word, self).get_queryset()\
            .prefetch_related('creator', 'definitions__contributor')

    def perform_create(self, serializer):
        """ Add the current connected user as creator """
        serializer.save(creator=self.request.user)

    def put(self, request, *args, **kwargs):
        """ Retrieve a word with its ID and update it """
        message = self.check_word_id()
        if message is not None:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        word_id = request.data.pop('word')
        queryset = models.Word.objects.all()
        word = get_object_or_404(queryset, id=word_id)
        serializer = serializers.Word(
            word, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        ---
        parameters:
            - name: search
              paramType: query
        """
        return super(Word, self).list(request, *args, **kwargs)


class Definition(viewsets.ModelViewSet, generics.CreateAPIView,
                 generics.DestroyAPIView, Checks):
    queryset = models.Definition.objects.all()
    serializer_class = serializers.Definition
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = DefinitionCursorPagination

    def get_queryset(self):
        return super(Definition, self).get_queryset()\
            .prefetch_related('contributor', 'word')

    def perform_create(self, serializer):
        """ Add the current connected user as contributor """
        message = self.check_word_id()
        if message is not None:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(contributor=self.request.user,
                        word=self.request.data['word'])

    def create(self, request, *args, **kwargs):
        """ Create the word """
        message = self.check_word_id()
        if message is not None:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        return super(Definition, self).create(request, *args, **kwargs)
