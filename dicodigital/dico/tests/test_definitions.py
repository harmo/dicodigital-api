from .utils import TestUtils


class TestDefinitionCreate(TestUtils):

    def setUp(self):
        super(TestDefinitionCreate, self).setUp()
        self.c.force_authenticate(user=self.user)

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

    def test_add_definition_to_none_word(self):
        response = self.create_definition(api_return=True)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'word parameter is missing')

    def test_add_definition_to_existant_word(self):
        word = self.create_word(api_return=True)

        definition = self.create_definition(word, api_return=True)

        self.assertEqual(definition.status_code, 201)
        self.assertEqual(word.data['url'], definition.data['word'])

    def test_definition_contributor_different_than_word_creator(self):
        word = self.create_word(api_return=True)
        self.c.logout()
        self.c.force_authenticate(user=self.user2)

        definition = self.create_definition(word=word, api_return=True)

        self.assertNotEqual(
            definition.data['contributor'], word.data['creator']
        )

    def test_if_definition_is_primary_only_if_first_added(self):
        word = self.create_word(api_return=True)
        self.create_definition(word=word, api_return=True)

        definition = self.create_definition(
            word=word,
            definition='this is a second definition',
            api_return=True
        )

        self.assertFalse(definition.data['is_primary'])


class TestDefinitionUpdate(TestUtils):

    def setUp(self):
        super(TestDefinitionUpdate, self).setUp()
        self.c.force_authenticate(user=self.user)

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
        word = self.create_word(api_return=True)
        definition = self.create_definition(word=word, api_return=True)
        definition_updated = {
            'text': 'this is the updated definition',
            'definition': definition.data['id']
        }

        response = self.update_definition(definition_updated)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'this is the updated definition')
