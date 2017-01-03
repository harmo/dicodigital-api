# -*- coding: utf-8 -*-
from .utils import TestUtils
from .. import models


class AnonymousTest(TestUtils):

    def setUp(self):
        super(AnonymousTest, self).setUp()
        self.alternative_ip = '127.0.0.10'

    def test_cant_post(self):
        response = self.c.post(self.url_word_list)
        self.assertEqual(response.status_code, 403)

    def test_can_list(self):
        response = self.c.get(self.url_word_list)
        self.assertEqual(response.status_code, 200)

    def test_search_word_by_label(self):
        models.Word.objects.create(
            label='test word', creator=self.user)
        response = self.c.get(self.url_word_search('test word'))
        results = response.data.get('results')
        self.assertEqual(len(results), 1)
        self.assertContains(response, 'test word')
        response = self.c.get(self.url_word_search('unexistant word'))
        self.assertEqual(len(response.data.get('results')), 0)

    def test_search_word_by_creator(self):
        models.Word.objects.create(
            label='test word', creator=self.user)
        response = self.c.get(self.url_word_search_by_creator('test_user'))
        results = response.data.get('results')
        self.assertEqual(len(results), 1)
        self.assertContains(response, 'test word')
        response = self.c.get(self.url_word_search_by_creator('unexistant_user'))
        self.assertEqual(len(response.data.get('results')), 0)


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

    def test_search_word_by_label(self):
        data = {'label': 'test word'}
        self.c.post(self.url_word_list, data, format='json')
        response = self.c.get(self.url_word_search('test word'))
        results = response.data.get('results')
        self.assertEqual(len(results), 1)
        self.assertContains(response, data['label'])

    def test_search_word_by_creator(self):
        data = {'label': 'test word'}
        self.c.post(self.url_word_list, data, format='json')
        response = self.c.get(self.url_word_search_by_creator('test_user'))
        results = response.data.get('results')
        self.assertEqual(len(results), 1)
        self.assertContains(response, 'test word')
        response = self.c.get(self.url_word_search_by_creator('unexistant_user'))
        self.assertEqual(len(response.data.get('results')), 0)

    def test_word_update(self):
        data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, data, format='json')
        update_data = {'label': 'test word (updated)', 'word': word_response.data['id']}
        response = self.c.put(self.url_word_list, update_data, format='json')
        self.assertEqual(response.data['label'], update_data['label'])
        response = self.c.get(self.url_word_search('test word'))
        self.assertEqual(len(response.data.get('results')), 0)
        response = self.c.get(self.url_word_search('test word (updated)'))
        results = response.data.get('results')
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]['label'], data['label'])

    def test_word_label_empty(self):
        data = {'label': ''}
        response = self.c.post(self.url_word_list, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_label_update_word_not_gt_0(self):
        data = {'label': 'test word'}
        self.c.post(self.url_word_list, data, format='json')
        update_data = {'label': 'test word (updated)', 'word': 0}
        response = self.c.put(self.url_word_list, update_data, format='json')
        self.assertEqual(response.status_code, 400)

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
        definition_data = {'text': 'this is the definition', 'word': word_response.data['id']}
        definition_response = self.c.post(self.url_definition_list, definition_data, format='json')
        self.assertEqual(definition_response.status_code, 201)
        self.assertEqual(word_response.data['url'], definition_response.data['word'])

    def test_definition_contributor_different_than_word_creator(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        self.c.logout()
        self.c.force_authenticate(user=self.user2)
        definition_data = {'text': 'this is the definition', 'word': word_response.data['id']}
        definition_response = self.c.post(self.url_definition_list, definition_data, format='json')
        self.assertNotEqual(definition_response.data['contributor'], word_response.data['creator'])

    def test_if_definition_is_primary_only_if_first_added(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        definition_data = {'text': 'this is the definition', 'word': word_response.data['id']}
        definition_response = self.c.post(self.url_definition_list, definition_data, format='json')
        self.assertTrue(definition_response.data['is_primary'])
        definition_data = {'text': 'this is a second definition', 'word': word_response.data['id']}
        definition_response = self.c.post(self.url_definition_list, definition_data, format='json')
        self.assertFalse(definition_response.data['is_primary'])
        response = self.c.get(self.url_word_search('test word'))
        results = response.data.get('results')
        self.assertEqual(len(results[0]['definitions']), 2)
        self.assertTrue(results[0]['definitions'][0]['is_primary'])
        self.assertFalse(results[0]['definitions'][1]['is_primary'])

    def test_definition_update_with_missing_id(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        definition_data = {'text': 'this is the definition', 'word': word_response.data['id']}
        self.c.post(self.url_definition_list, definition_data, format='json')
        definition_updated = {'text': 'this is the updated definition'}
        response = self.c.put(self.url_definition_list, definition_updated)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'definition parameter is missing')

    def test_definition_update_with_none_id(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        definition_data = {'text': 'this is the definition', 'word': word_response.data['id']}
        self.c.post(self.url_definition_list, definition_data, format='json')
        definition_updated = {'text': 'this is the updated definition', 'definition': ''}
        response = self.c.put(self.url_definition_list, definition_updated)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'definition ID cannot be None')

    def test_definition_update_with_unknow_id(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        definition_data = {'text': 'this is the definition', 'word': word_response.data['id']}
        self.c.post(self.url_definition_list, definition_data, format='json')
        definition_updated = {'text': 'this is the updated definition', 'definition': 0}
        response = self.c.put(self.url_definition_list, definition_updated)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'definition ID must be an integer > 0')

    def test_definition_update_successful(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        definition_data = {'text': 'this is the definition', 'word': word_response.data['id']}
        def_response = self.c.post(self.url_definition_list, definition_data, format='json')
        definition_updated = {'text': 'this is the updated definition', 'definition': def_response.data['id']}
        response = self.c.put(self.url_definition_list, definition_updated, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'this is the updated definition')

    def test_search_word_by_first_letter(self):
        data = {'label': 'a word'}
        self.c.post(self.url_word_list, data, format='json')
        data = {'label': 'test word'}
        self.c.post(self.url_word_list, data, format='json')
        search = self.c.get(self.url_word_search_by_first_letter('t'))
        results = search.data.get('results')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['label'], data['label'])
        search = self.c.get(self.url_word_search_by_first_letter('a'))
        results = search.data.get('results')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['label'], 'a word')
        search = self.c.get(self.url_word_search_by_first_letter('z'))
        results = search.data.get('results')
        self.assertEqual(len(results), 0)

    def test_search_word_by_plain_text_in_definition(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        definition_data = {'text': 'this is the definition', 'word': word_response.data['id']}
        self.c.post(self.url_definition_list, definition_data, format='json')
        definition_data['text'] = 'another definition'
        self.c.post(self.url_definition_list, definition_data, format='json')
        word2_data = {'label': 'second test word'}
        word2_response = self.c.post(self.url_word_list, word2_data, format='json')
        definition2_data = {'text': 'again one definition', 'word': word2_response.data['id']}
        self.c.post(self.url_definition_list, definition2_data, format='json')
        search = self.c.get(self.url_word_search_by_definition('the definition'))
        results = search.data.get('results')
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]['definitions']), 2)
        search = self.c.get(self.url_word_search_by_definition('again one'))
        results = search.data.get('results')
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]['definitions']), 1)
        search = self.c.get(self.url_word_search_by_definition('an inexistant one'))
        results = search.data.get('results')
        self.assertEqual(len(results), 0)

    def test_search_words_without_definition(self):
        word_data = {'label': 'test word'}
        word_response = self.c.post(self.url_word_list, word_data, format='json')
        definition_data = {'text': 'this is the definition', 'word': word_response.data['id']}
        self.c.post(self.url_definition_list, definition_data, format='json')
        search = self.c.get(self.url_word_search_without_definition('True'))
        results = search.data.get('results')
        self.assertEqual(len(results), 0)
        word2_data = {'label': 'second test word'}
        self.c.post(self.url_word_list, word2_data, format='json')
        search = self.c.get(self.url_word_search_without_definition('True'))
        results = search.data.get('results')
        self.assertEqual(len(results), 1)
        search = self.c.get(self.url_word_search_without_definition('False'))
        results = search.data.get('results')
        self.assertEqual(len(results), 1)

    def test_get_one_random_word(self):
        for i in range(1, 200):
            word_data = {'label': 'test word {}'.format(i)}
            self.c.post(self.url_word_list, word_data, format='json')
        for i in range(1, 10):
            response = self.c.get(self.url_get_random_word())
            results = response.data.get('results')
            self.assertEqual(len(results), 1)

    def test_get_one_random_word_on_filtered_words(self):
        word_data = {'label': 'first word'}
        self.c.post(self.url_word_list, word_data, format='json')
        word_data = {'label': 'second word'}
        self.c.post(self.url_word_list, word_data, format='json')
        word_data = {'label': 'third word'}
        self.c.post(self.url_word_list, word_data, format='json')
        response = self.c.get(self.url_word_list + '?first=s&random')
        results = response.data.get('results')
        self.assertEqual(len(results), 1)
        response = self.c.get(self.url_word_list + '?label=inexistant&random')
        results = response.data.get('results')
        self.assertEqual(len(results), 0)
