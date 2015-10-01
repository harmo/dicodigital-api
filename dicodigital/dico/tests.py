# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class AnonymousTest(TestCase):

    def setUp(self):
        super(AnonymousTest, self).setUp()
        self.user = get_user_model().objects.create(username='test_user')
        self.c = APIClient()

    def test_cant_post(self):
        response = self.c.post('/word/')
        self.assertEqual(response.status_code, 403)
