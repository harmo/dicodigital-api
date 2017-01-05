from unittest.mock import Mock

from .utils import TestUtils


class TestAnonymousWordSearch(TestUtils):

    def test_can_list(self):
        response = self.c.get(self.url_word_list)

        self.assertEqual(response.status_code, 200)

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


class TestAnonymousWordCreate(TestUtils):

    def test_cant_post(self):
        response = self.c.post(self.url_word_list)

        self.assertEqual(response.status_code, 403)

    def test_cant_update(self):
        response = self.c.put(self.url_word_list)

        self.assertEqual(response.status_code, 403)


class TestConnectedWordSearch(TestUtils):

    def setUp(self):
        super(TestConnectedWordSearch, self).setUp()
        self.c.force_authenticate(user=self.user)

    def test_can_list_after_login(self):
        response = self.c.get(self.url_word_list)

        self.assertEqual(response.status_code, 200)

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


class TestConnectedWordCreate(TestUtils):

    def setUp(self):
        super(TestConnectedWordCreate, self).setUp()
        self.c.force_authenticate(user=self.user)

    def test_can_post_after_login(self):
        response = self.c.post(self.url_word_list)

        self.assertEqual(response.status_code, 400)

    def test_creator_linked_during_word_creation(self):
        data = {'label': self.word_label}

        response = self.c.post(self.url_word_list, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['label'], data['label'])
        self.assertEqual(response.data['creator'], self.user.username)


class TestConnectedWordUpdate(TestUtils):

    word_updated_label = 'test_word (updated)'

    def setUp(self):
        super(TestConnectedWordUpdate, self).setUp()
        self.c.force_authenticate(user=self.user)

    def update_word(self, word=None):
        updated_data = {'label': self.word_updated_label}
        if word:
            updated_data['word'] = word.data['id']

        return self.c.put(self.url_word_list, updated_data, format='json')

    def test_when_word_updated_it_returns_updated_one(self):
        word = self.create_word(api_return=True)

        response = self.update_word(word)

        self.assertEqual(response.data['label'], self.word_updated_label)

    def test_when_word_updated_it_dont_returns_original_one(self):
        word = self.create_word(api_return=True)
        self.update_word(word)

        response = self.c.get(self.url_word_search(self.word_label))

        self.assertEqual(len(response.data.get('results')), 0)

    def test_updated_word_is_found(self):
        word = self.create_word(api_return=True)
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


class TestSpecialWordSearch(TestUtils):

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


class TestGetRandomWords(TestUtils):

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
