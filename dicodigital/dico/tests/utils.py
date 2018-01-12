from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient

from ..models import Word, Definition


class TestUtils(TestCase):

    word_label = 'test word'

    def setUp(self):
        super(TestUtils, self).setUp()
        self.user = get_user_model().objects.create(
            username='test_user', password='test')
        self.user2 = get_user_model().objects.create(
            username='test_user2', password='test')
        self.c = APIClient()
        self.url_word_list = reverse('word-list')
        self.url_definition_list = reverse('definition-list')
        self.url_vote_list = reverse('vote-list')

    def url_word_by_id(self, id):
        return '{url}{id}'.format(
            url=self.url_word_list, id=id)

    def url_word_search(self, label):
        return self.url_word_list + '?label=' + label

    def url_word_search_by_creator(self, creator):
        return self.url_word_list + '?creator=' + creator

    def url_word_search_by_first_letter(self, letter):
        return self.url_word_list + '?first=' + letter

    def url_word_search_by_definition(self, word):
        return self.url_word_list + '?def_like=' + word

    def url_word_search_without_definition(self, str_bool):
        return self.url_word_list + '?empty=' + str_bool

    def url_get_random_word(self):
        return self.url_word_list + '?random=True'

    def create_word(self, label=None, api_return=False):
        if not api_return:
            return Word.objects.create(
                label=label if label else self.word_label,
                creator=self.user
            )

        else:
            return self.c.post(
                self.url_word_list,
                {'label': self.word_label if not label else label},
                format='json'
            )

    def create_definition(self, word=None, definition=None, api_return=False):
        text = definition if definition else 'this is the definition'

        if not api_return:
            if not word:
                return None

            return Definition.objects.create(
                contributor=self.user,
                word=word,
                text=text
            )

        else:
            data = {'text': text}

            if word:
                data['word'] = word.data['id']

            return self.c.post(
                self.url_definition_list,
                data,
                format='json'
            )
