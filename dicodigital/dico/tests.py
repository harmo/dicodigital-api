# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class TestUtils(TestCase):

    def setUp(self):
        super(TestUtils, self).setUp()
        self.user = get_user_model().objects.create(
            username='test_user', password='test')
        self.c = APIClient()
        self.url_word_list = reverse('word-list')


class AnonymousTest(TestUtils):

    def test_cant_post(self):
        response = self.c.post(self.url_word_list)
        self.assertEqual(response.status_code, 403)

    def test_can_list(self):
        response = self.c.get(self.url_word_list)
        self.assertEqual(response.status_code, 200)


class ConnectedTest(TestUtils):

    def setUp(self):
        super(ConnectedTest, self).setUp()
        self.c.force_authenticate(user=self.user)

    def test_can_post_after_login(self):
        response = self.c.post(self.url_word_list)
        self.assertEqual(response.status_code, 400)

    def test_can_list_after_login(self):
        response = self.c.get(self.url_word_list)
        self.assertEqual(response.status_code, 200)

    def test_creator_linked_during_word_creation(self):
        data = {'label': 'test word'}
        response = self.c.post(self.url_word_list, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['label'], data['label'])
        self.assertEqual(response.data['creator'], self.user.username)

    def test_word_auto_slug(self):
        data = {'label': 'test word'}
        self.c.post(self.url_word_list, data, format='json')
        response = self.c.get('/word/test-word/')
        self.assertEqual(response.status_code, 200)

    def test_word_update(self):
        data = {'label': 'test word'}
        self.c.post(self.url_word_list, data, format='json')
        update_data = {'label': 'test word (updated)', 'word': 'test-word'}
        response = self.c.put(self.url_word_list, update_data, format='json')
        self.assertEqual(response.data['label'], update_data['label'])
        response = self.c.get(self.url_word_list + 'test-word/')
        self.assertNotEqual(response.data['label'], data['label'])

    def test_word_label_empty(self):
        data = {'label': ''}
        response = self.c.post(self.url_word_list, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_label_update_word_not_found(self):
        data = {'label': 'test word'}
        self.c.post(self.url_word_list, data, format='json')
        update_data = {'label': 'test word (updated)', 'word': 'word-does-not-exist'}
        response = self.c.put(self.url_word_list, update_data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_add_empty_definition_to_new_word(self):
        data = {'label': 'test word',
                'definitions': [{}]}
        response = self.c.post(self.url_word_list, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_creator_linked_during_add_definition_to_new_word(self):
        data = {'label': 'test word',
                'definitions': [{'text': 'this is the definition'}]}
        response = self.c.post(self.url_word_list, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['definitions']), 1)
        self.assertEqual(response.data['creator'], response.data['definitions'][0]['contributor'])

    def test_add_multiples_definitions_to_new_word(self):
        data = {'label': 'test word',
                'definitions': [{'text': 'this is the definition'},
                                {'text': 'this is another definition'}]}
        response = self.c.post(self.url_word_list, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['definitions']), 2)

    def test_primary_definition_was_set_during_add_definitions_to_new_word(self):
        data = {'label': 'test word',
                'definitions': [{'text': 'this is the definition'},
                                {'text': 'this is another definition'}]}
        response = self.c.post(self.url_word_list, data, format='json')
        self.assertTrue(response.data['definitions'][0]['is_primary'])
