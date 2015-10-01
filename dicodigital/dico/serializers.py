from rest_framework import serializers
from . import models


class Definition(serializers.ModelSerializer):
    class Meta:
        model = models.Definition
        fields = ('text', 'contributor',
                  'is_primary', 'created_at')


class Word(serializers.ModelSerializer):
    definitions = Definition(many=True)

    class Meta:
        model = models.Word
        fields = ('label', 'creator',
                  'created_at', 'definitions')
