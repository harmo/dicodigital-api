# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class TestUtils(TestCase):

    def setUp(self):
        super(TestUtils, self).setUp()
        self.user = get_user_model().objects.create(
            username='test_user', password='test')
        self.c = APIClient()


class AnonymousTest(TestUtils):

    def test_cant_post(self):
        response = self.c.post('/word/')
        self.assertEqual(response.status_code, 403)

    def test_can_list(self):
        response = self.c.get('/word/')
        self.assertEqual(response.status_code, 200)


class ConnectedTest(TestUtils):

    def setUp(self):
        super(ConnectedTest, self).setUp()
        self.c.force_authenticate(user=self.user)

    def test_can_post_after_login(self):
        response = self.c.post('/word/')
        self.assertEqual(response.status_code, 400)

    def test_can_list_after_login(self):
        response = self.c.get('/word/')
        self.assertEqual(response.status_code, 200)

    def test_creator_linked_during_word_creation(self):
        data = {'label': 'test word'}
        response = self.c.post('/word/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['label'], data['label'])
        self.assertEqual(response.data['creator'], self.user.username)
