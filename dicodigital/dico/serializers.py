from rest_framework import serializers
from . import models


class Word(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField('word-detail', source='id', read_only=True)

    class Meta:
        model = models.Word
        fields = ('id', 'label', 'url')
