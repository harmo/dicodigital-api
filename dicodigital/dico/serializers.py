from rest_framework import serializers

from . import models


class Definition(serializers.ModelSerializer):
    contributor = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    word = serializers.HyperlinkedRelatedField(
        view_name='word-detail',
        lookup_field='id',
        read_only=True)

    class Meta:
        model = models.Definition
        fields = ('id', 'word', 'text', 'contributor',
                  'is_primary', 'created_at')

    def create(self, validated_data):
        word_id = validated_data.pop('word')
        word = models.Word.objects.get(id=word_id)
        is_primary = True
        if word.definitions.count() > 0:
            is_primary = False
        return models.Definition.objects.create(
            word=word,
            is_primary=is_primary,
            **validated_data)


class Word(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='word-detail',
        lookup_field='id',
        read_only=True)
    definitions = Definition(many=True, required=False)
    creator = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = models.Word
        fields = ('id', 'label', 'creator', 'url',
                  'created_at', 'definitions')

    def create(self, validated_data):
        definitions = []
        if 'definitions' in validated_data:
            definitions = validated_data.pop('definitions')
        word = models.Word.objects.create(**validated_data)
        for definition in definitions:
            is_primary = True if definition == definitions[0] else False
            models.Definition.objects.create(
                word=word,
                contributor=word.creator,
                is_primary=is_primary,
                **definition)
        return word


class Vote(serializers.ModelSerializer):
    definition = serializers.HyperlinkedRelatedField(
        view_name='definition-detail',
        lookup_field='id',
        read_only=True)

    class Meta:
        model = models.Vote
        fields = ('id', 'definition', 'score', 'created_at',
                  'user', 'ip_address', 'cookie')
