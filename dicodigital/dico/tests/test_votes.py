# -*- coding: utf-8 -*-
import json

from .utils import TestUtils
from ..models import Definition, Vote


class TestAnonymousVote(TestUtils):

    def test_anonymous_user_can_list_votes(self):
        response = self.c.get(self.url_vote_list)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_has_permission_to_post(self):
        response = self.c.post(self.url_vote_list)

        self.assertNotEqual(response.status_code, 403)

    def test_ip_adress_is_already_registered(self):
        word = self.create_word(label='a word')
        definition = self.create_definition(word=word)
        ip_address = '0.0.0.0'
        first_vote = Vote.objects.create(
            definition=definition,
            ip_address=ip_address,
            score=1
        )
        data = {
            'definition': definition.pk,
            'ip_address': ip_address,
            'score': 1
        }

        response = self.c.post(self.url_vote_list, data, format='json')

        self.assertEqual(
            response.data,
            'user has already voted with IP %s (%s)' % (
                ip_address,
                first_vote.created_at
            )
        )


class TestConnectedVote(TestUtils):

    def setUp(self):
        super(TestConnectedVote, self).setUp()
        self.c.force_authenticate(user=self.user)

    def create_word_and_definition(self):
        word = self.create_word(label='a word', api_return=True)
        return self.create_definition(word=word, api_return=True)

    def test_missing_ip_address(self):
        response = self.c.post(self.url_vote_list)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'missing IP address')

    def test_missing_definition_parameter_during_post(self):
        data = {'ip_address': '0.0.0.0'}
        response = self.c.post(self.url_vote_list, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'definition parameter is missing')

    def test_definition_id_must_not_be_zero(self):
        data = {'definition': 0}

        response = self.c.post(self.url_vote_list, data, format='json')

        self.assertEqual(response.status_code, 400)

    def vote(self, definition, ip_address='0.0.0.0', score=1):
        data = {
            'definition': definition.data['id'],
            'ip_address': ip_address,
            'score': score
        }
        return self.c.post(self.url_vote_list, data, format='json')

    def test_add_1_to_score(self):
        definition = self.create_word_and_definition()
        self.vote(definition)

        definition = Definition.objects.get(id=definition.data['id'])

        self.assertEqual(definition.score, 1)

    def test_add_10_to_score(self):
        definition = self.create_word_and_definition()
        for i in range(0, 10):
            ip_address = '0.0.0.%s' % i
            self.vote(definition=definition, ip_address=ip_address)

        definition = Definition.objects.get(id=definition.data['id'])

        self.assertEqual(definition.score, 10)

    def test_remove_1_to_score(self):
        definition = self.create_word_and_definition()
        self.vote(definition, score=-1)

        definition = Definition.objects.get(id=definition.data['id'])

        self.assertEqual(definition.score, -1)

    def test_remove_10_to_score(self):
        definition = self.create_word_and_definition()
        for i in range(0, 10):
            ip_address = '0.0.0.%s' % i
            self.vote(definition, score=-1, ip_address=ip_address)

        definition = Definition.objects.get(id=definition.data['id'])

        self.assertEqual(definition.score, -10)

    def test_definition_has_vote_in_response(self):
        definition = self.create_word_and_definition()
        self.vote(definition, score=1, ip_address='0.0.0.0')
        vote = self.c.get(self.url_vote_list, {'id': 1})

        response = self.c.get(self.url_definition_list, {'id': 1})

        self.assertContains(response, vote.content)
