# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, permissions, status, viewsets
from rest_framework.response import Response

from . import filters as my_filters, models, serializers


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
        """Check if <keyword> parameter is in data."""
        if keyword not in self.request.data:
            return '{} parameter is missing'.format(keyword)

        """Check if <keyword> parameter is not None."""
        if self.request.data[keyword] == '':
            return '{} ID cannot be None'.format(keyword)

        """Check if <keyword> parameter is > 0."""
        if int(self.request.data[keyword]) < 1:
            return '{} ID must be an integer > 0'.format(keyword)

    def check_word_id(self):
        message = self._check_id('word')
        if message:
            return message

    def check_definition_id(self):
        message = self._check_id('definition')
        if message:
            return message


class Word(viewsets.ModelViewSet, Checks):
    queryset = models.Word.objects.all()
    serializer_class = serializers.Word
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    pagination_class = WordCursorPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = my_filters.WordFilter

    def get_queryset(self):
        return super(Word, self).get_queryset()\
            .prefetch_related('creator', 'definitions__contributor')

    def perform_create(self, serializer):
        """Add the current connected user as creator."""
        serializer.save(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create the word."""
        return super(Word, self).create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Retrieve a word with its ID and update it."""
        message = self.check_word_id()
        if message:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        queryset = models.Word.objects.all()
        word = get_object_or_404(queryset, id=request.data.get('word'))

        serializer = serializers.Word(
            word, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Search a word with label."""
        return super(Word, self).list(request, *args, **kwargs)


class Definition(viewsets.ModelViewSet, Checks):
    queryset = models.Definition.objects.all()
    serializer_class = serializers.Definition
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = DefinitionCursorPagination

    def get_queryset(self):
        return super(Definition, self).get_queryset()\
            .prefetch_related('contributor', 'word', 'votes')

    def perform_create(self, serializer):
        """Add the current connected user as contributor."""
        message = self.check_word_id()
        if message:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(
            contributor=self.request.user,
            word=self.request.data['word']
        )

    def create(self, request, *args, **kwargs):
        """Create the definition, with the word."""
        message = self.check_word_id()
        if message:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        return super(Definition, self).create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Retrieve a definition with its ID and update it."""
        message = self.check_definition_id()
        if message:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        queryset = models.Definition.objects.all()
        definition = get_object_or_404(
            queryset, id=request.data.get('definition')
        )

        serializer = serializers.Definition(
            definition, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class Vote(viewsets.ModelViewSet, Checks):
    queryset = models.Vote.objects.all()
    serializer_class = serializers.Vote
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        """Add the current connected user as voter."""
        serializer.save(
            user=self.request.user,
            definition=self.request.data['definition']
        )

    def create(self, request, *args, **kwargs):
        """Add a vote, with the definition."""
        error = self.make_checks()
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return super(Vote, self).create(request, *args, **kwargs)

    def make_checks(self):
        error = self.check_ip_address()
        if not error:
            error = self.check_definition_id()

        return error or None

    def check_ip_address(self):
        if not self.request.data.get('ip_address'):
            return 'missing IP address'

        try:
            vote = models.Vote.objects.get(
                definition__id=self.request.data.get('definition'),
                ip_address=self.request.data.get('ip_address')
            )
            return 'user has already voted with IP %s (%s)' % (
                vote.ip_address, vote.created_at
            )

        except models.Vote.DoesNotExist:
            pass
