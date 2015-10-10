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
        self.user2 = get_user_model().objects.create(
            username='test_user2', password='test')
        self.c = APIClient()
        self.url_word_list = reverse('word-list')
        self.url_definition_list = reverse('definition-list')


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

    def test_word_update_on_none_word(self):
        data = {'label': 'test word'}
        self.c.post(self.url_word_list, data, format='json')
        update_data = {'label': 'test word (updated)'}
        response = self.c.put(self.url_word_list, update_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'word parameter is missing')

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

    def test_add_definition_to_none_word(self):
        data = {'text': 'this is the definition'}
        response = self.c.post(self.url_definition_list, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'word parameter is missing')

    def test_add_definition_to_existant_word(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        definition_data = {'text': 'this is the definition', 'word': 'test-word'}
        definition_response = self.c.post(self.url_definition_list, definition_data, format='json')
        self.assertEqual(definition_response.status_code, 201)
        self.assertEqual(word_response.data['url'], definition_response.data['word'])

    def test_definition_contributor_different_than_word_creator(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        self.c.logout()
        self.c.force_authenticate(user=self.user2)
        definition_data = {'text': 'this is the definition', 'word': 'test-word'}
        definition_response = self.c.post(self.url_definition_list, definition_data, format='json')
        self.assertNotEqual(definition_response.data['contributor'], word_response.data['creator'])

    def test_if_definition_is_primary_only_if_first_added(self):
        word_data = {'label': 'test word'}
        self.c.post(self.url_word_list, word_data, format='json')
        definition_data = {'text': 'this is the definition', 'word': 'test-word'}
        definition_response = self.c.post(self.url_definition_list, definition_data, format='json')
        self.assertTrue(definition_response.data['is_primary'])
        definition_data = {'text': 'this is a second definition', 'word': 'test-word'}
        definition_response = self.c.post(self.url_definition_list, definition_data, format='json')
        self.assertFalse(definition_response.data['is_primary'])
        response = self.c.get(self.url_word_list + 'test-word/')
        self.assertEqual(len(response.data['definitions']), 2)
        self.assertTrue(response.data['definitions'][0]['is_primary'])
        self.assertFalse(response.data['definitions'][1]['is_primary'])
