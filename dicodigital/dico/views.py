# -*- coding: utf-8 -*-
from rest_framework import viewsets, permissions, status, pagination, filters
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

    def _check_id(self, keyword):
        """ Check if <keyword> parameter is in data """
        if keyword not in self.request.data:
            return '{} parameter is missing'.format(keyword)
        """ Check if <keyword> parameter is not None """
        if self.request.data[keyword] == '':
            return '{} ID cannot be None'.format(keyword)
        """ Check if <keyword> parameter is > 0 """
        if int(self.request.data[keyword]) < 1:
            return '{} ID must be an integer > 0'.format(keyword)

    def check_word_id(self):
        message = self._check_id('word')
        if message is not None:
            return message

    def check_definition_id(self):
        message = self._check_id('definition')
        if message is not None:
            return message


class Word(viewsets.ModelViewSet, Checks):
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

    def create(self, request, *args, **kwargs):
        """ Create the word """
        return super(Word, self).create(request, *args, **kwargs)

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
        Search a word with label
        ---
        parameters:
            - name: search
              paramType: query
        """
        return super(Word, self).list(request, *args, **kwargs)


class Definition(viewsets.ModelViewSet, Checks):
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
        """ Create the definition, with the word """
        message = self.check_word_id()
        if message is not None:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        return super(Definition, self).create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """ Retrieve a definition with its ID and update it """
        message = self.check_definition_id()
        if message is not None:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        definition_id = request.data.pop('definition')
        queryset = models.Definition.objects.all()
        definition = get_object_or_404(queryset, id=definition_id)
        serializer = serializers.Definition(
            definition, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
