# -*- coding: utf-8 -*-
from unittest.mock import Mock

from .utils import TestUtils
from .. import models


class AnonymousTest(TestUtils):

    def setUp(self):
        super(AnonymousTest, self).setUp()

    def test_cant_post(self):
        response = self.c.post(self.url_word_list)

        self.assertEqual(response.status_code, 403)

    def test_can_list(self):
        response = self.c.get(self.url_word_list)

        self.assertEqual(response.status_code, 200)

    def create_word(self):
        models.Word.objects.create(label='test word', creator=self.user)

    def test_search_existant_word_by_label(self):
        self.create_word()

        response = self.c.get(self.url_word_search('test word'))

        self.assertEqual(len(response.data.get('results')), 1)
        self.assertContains(response, 'test word')

    def test_search_unexistant_word_by_label(self):
        self.create_word()

        response = self.c.get(self.url_word_search('unexistant word'))

        self.assertEqual(len(response.data.get('results')), 0)

    def test_search_existant_word_by_creator(self):
        self.create_word()

        response = self.c.get(self.url_word_search_by_creator('test_user'))

        self.assertEqual(len(response.data.get('results')), 1)
        self.assertContains(response, 'test word')

    def test_search_unexistant_word_by_creator(self):
        self.create_word()

        response = self.c.get(self.url_word_search_by_creator('unexistant'))

        self.assertEqual(len(response.data.get('results')), 0)


class ConnectedTest(TestUtils):

    word_label = 'test_word'
    word_updated_label = 'test_word (updated)'

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
        data = {'label': self.word_label}

        response = self.c.post(self.url_word_list, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['label'], data['label'])
        self.assertEqual(response.data['creator'], self.user.username)

    def test_search_word_by_label(self):
        data = {'label': self.word_label}
        self.c.post(self.url_word_list, data, format='json')

        response = self.c.get(self.url_word_search(self.word_label))

        self.assertEqual(len(response.data.get('results')), 1)
        self.assertContains(response, data['label'])

    def test_search_existant_word_by_creator(self):
        data = {'label': self.word_label}
        self.c.post(self.url_word_list, data, format='json')

        response = self.c.get(self.url_word_search_by_creator('test_user'))

        self.assertEqual(len(response.data.get('results')), 1)
        self.assertContains(response, self.word_label)

    def test_search_unexistant_word_by_creator(self):
        data = {'label': self.word_label}
        self.c.post(self.url_word_list, data, format='json')

        response = self.c.get(self.url_word_search_by_creator('unexistant'))

        self.assertEqual(len(response.data.get('results')), 0)

    def create_word(self, label=''):
        return self.c.post(
            self.url_word_list,
            {'label': self.word_label if not label else label},
            format='json'
        )

    def update_word(self, word=None):
        updated_data = {'label': self.word_updated_label}
        if word:
            updated_data['word'] = word.data['id']

        return self.c.put(self.url_word_list, updated_data, format='json')

    def test_when_word_updated_it_returns_updated_one(self):
        word = self.create_word()

        response = self.update_word(word)

        self.assertEqual(response.data['label'], self.word_updated_label)

    def test_when_word_updated_it_dont_returns_original_one(self):
        word = self.create_word()
        self.update_word(word)

        response = self.c.get(self.url_word_search(self.word_label))

        self.assertEqual(len(response.data.get('results')), 0)

    def test_updated_word_is_found(self):
        word = self.create_word()
        self.update_word(word)

        response = self.c.get(self.url_word_search(self.word_updated_label))

        self.assertEqual(len(response.data.get('results')), 1)

    def test_word_label_empty(self):
        data = {'label': ''}

        response = self.c.post(self.url_word_list, data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_word_label_update_id_must_not_be_zero(self):
        word = Mock(data={'id': 0})

        response = self.update_word(word)

        self.assertEqual(response.status_code, 400)

    def test_word_update_on_none_word(self):
        response = self.update_word()

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.data, 'word parameter is missing')

    def create_word_with_definitions(self, definitions=[{}]):
        data = {
            'label': self.word_label,
            'definitions': definitions
        }

        return self.c.post(self.url_word_list, data, format='json')

    def test_add_empty_definition_to_new_word(self):
        response = self.create_word_with_definitions()

        self.assertEqual(response.status_code, 400)

    def test_creator_linked_during_add_definition_to_new_word(self):
        response = self.create_word_with_definitions(
            definitions=[{'text': 'this is the definition'}]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['definitions']), 1)
        self.assertEqual(
            response.data['creator'],
            response.data['definitions'][0]['contributor']
        )

    def test_add_multiples_definitions_to_new_word(self):
        response = self.create_word_with_definitions(
            definitions=[
                {'text': 'this is the definition'},
                {'text': 'this is another definition'}
            ]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['definitions']), 2)

    def test_primary_definition_was_set_during_add_multiple_to_new_word(self):
        response = self.create_word_with_definitions(
            definitions=[
                {'text': 'this is the definition'},
                {'text': 'this is another definition'}
            ]
        )

        self.assertTrue(response.data['definitions'][0]['is_primary'])

    def create_definition(self, word=None, definition=None):
        data = {
            'text': 'this is the definition' if not definition else definition
        }

        if word:
            data['word'] = word.data['id']

        return self.c.post(
            self.url_definition_list,
            data,
            format='json'
        )

    def test_add_definition_to_none_word(self):
        response = self.create_definition()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'word parameter is missing')

    def test_add_definition_to_existant_word(self):
        word = self.create_word()

        definition = self.create_definition(word)

        self.assertEqual(definition.status_code, 201)
        self.assertEqual(word.data['url'], definition.data['word'])

    def test_definition_contributor_different_than_word_creator(self):
        word = self.create_word()
        self.c.logout()
        self.c.force_authenticate(user=self.user2)

        definition = self.create_definition(word)

        self.assertNotEqual(
            definition.data['contributor'], word.data['creator']
        )

    def test_if_definition_is_primary_only_if_first_added(self):
        word = self.create_word()
        self.create_definition(word)

        definition = self.create_definition(
            word, definition='this is a second definition'
        )

        self.assertFalse(definition.data['is_primary'])

    def update_definition(self, definition=None):
        return self.c.put(self.url_definition_list, definition)

    def test_definition_update_with_missing_id(self):
        word = self.create_word()
        self.create_definition(word)
        definition_updated = {'text': 'this is the updated definition'}

        response = self.update_definition(definition_updated)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'definition parameter is missing')

    def test_definition_update_with_none_id(self):
        word = self.create_word()
        self.create_definition(word)
        definition_updated = {
            'text': 'this is the updated definition',
            'definition': ''
        }

        response = self.update_definition(definition_updated)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'definition ID cannot be None')

    def test_definition_update_with_unknow_id(self):
        word = self.create_word()
        self.create_definition(word)
        definition_updated = {
            'text': 'this is the updated definition',
            'definition': 0
        }

        response = self.update_definition(definition_updated)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'definition ID must be an integer > 0')

    def test_definition_update_successful(self):
        word = self.create_word()
        definition = self.create_definition(word)
        definition_updated = {
            'text': 'this is the updated definition',
            'definition': definition.data['id']
        }

        response = self.update_definition(definition_updated)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'this is the updated definition')

    def test_search_word_by_first_letter(self):
        self.create_word(label='a word')
        self.create_word(label=self.word_label)

        search = self.c.get(self.url_word_search_by_first_letter('t'))

        self.assertEqual(len(search.data.get('results')), 1)
        self.assertEqual(
            search.data.get('results')[0]['label'],
            self.word_label
        )

        search = self.c.get(self.url_word_search_by_first_letter('a'))

        self.assertEqual(len(search.data.get('results')), 1)
        self.assertEqual(search.data.get('results')[0]['label'], 'a word')

        search = self.c.get(self.url_word_search_by_first_letter('z'))

        self.assertEqual(len(search.data.get('results')), 0)

    def test_search_word_by_plain_text_in_definition(self):
        word = self.create_word()
        self.create_definition(word, definition='the definition')
        self.create_definition(word, definition='another definition')

        word2 = self.create_word('second test word')
        self.create_definition(word2, definition='again one definition')

        search = self.c.get(
            self.url_word_search_by_definition('the definition')
        )

        self.assertEqual(len(search.data.get('results')), 1)
        self.assertEqual(len(search.data.get('results')[0]['definitions']), 2)

        search = self.c.get(self.url_word_search_by_definition('again one'))

        self.assertEqual(len(search.data.get('results')), 1)
        self.assertEqual(len(search.data.get('results')[0]['definitions']), 1)

        search = self.c.get(
            self.url_word_search_by_definition('an inexistant one')
        )

        self.assertEqual(len(search.data.get('results')), 0)

    def test_search_words_without_definition(self):
        word = self.create_word()
        self.create_definition(word)

        search = self.c.get(self.url_word_search_without_definition('True'))

        self.assertEqual(len(search.data.get('results')), 0)

        self.create_word('second test word')

        search = self.c.get(self.url_word_search_without_definition('True'))

        self.assertEqual(len(search.data.get('results')), 1)

        search = self.c.get(self.url_word_search_without_definition('False'))

        self.assertEqual(len(search.data.get('results')), 1)

    def test_get_one_random_word(self):
        for i in range(1, 200):
            self.create_word('test word %s' % i)

        for i in range(1, 10):
            response = self.c.get(self.url_get_random_word())

            self.assertEqual(len(response.data.get('results')), 1)

    def test_get_one_random_word_on_filtered_words(self):
        self.create_word('first word')
        self.create_word('second word')
        self.create_word('third word')

        response = self.c.get(self.url_word_list + '?first=s&random')
        self.assertEqual(len(response.data.get('results')), 1)

        response = self.c.get(self.url_word_list + '?label=inexistant&random')
        self.assertEqual(len(response.data.get('results')), 0)
