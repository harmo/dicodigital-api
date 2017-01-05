# -*- coding: utf-8 -*-
from .utils import TestUtils
from .. import models


class TestAnonymousVote(TestUtils):

    def test_anonymous_user_can_list_votes(self):
        response = self.c.get(self.url_vote_list)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_has_permission_to_post(self):
        response = self.c.post(self.url_vote_list)

        self.assertNotEqual(response.status_code, 403)


class TestConnectedVote(TestUtils):

    def setUp(self):
        super(TestConnectedVote, self).setUp()
        self.c.force_authenticate(user=self.user)

    def create_word_and_definition(self):
        word = self.create_word(label='a word', api_return=True)
        return self.create_definition(word=word, api_return=True)

    def test_missing_definition_parameter_during_post(self):
        response = self.c.post(self.url_vote_list)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'definition parameter is missing')

    def test_definition_id_must_not_be_zero(self):
        data = {'definition': 0}

        response = self.c.post(self.url_vote_list, data, format='json')

        self.assertEqual(response.status_code, 400)

    def vote(self, definition, score=1):
        data = {'definition': definition.data['id'], 'score': score}
        self.c.post(self.url_vote_list, data, format='json')

    def test_add_1_to_score(self):
        definition = self.create_word_and_definition()
        self.vote(definition)

        definition = models.Definition.objects.get(id=definition.data['id'])

        self.assertEqual(definition.score, 1)

    def test_add_10_to_score(self):
        definition = self.create_word_and_definition()
        for i in range(0, 10):
            self.vote(definition)

        definition = models.Definition.objects.get(id=definition.data['id'])

        self.assertEqual(definition.score, 10)

    def test_remove_1_to_score(self):
        definition = self.create_word_and_definition()
        self.vote(definition, score=-1)

        definition = models.Definition.objects.get(id=definition.data['id'])

        self.assertEqual(definition.score, -1)

    def test_remove_10_to_score(self):
        definition = self.create_word_and_definition()
        for i in range(0, 10):
            self.vote(definition, score=-1)

        definition = models.Definition.objects.get(id=definition.data['id'])

        self.assertEqual(definition.score, -10)
