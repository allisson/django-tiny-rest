# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.utils.encoding import smart_text
from django.contrib.auth import get_user_model

from tiny_rest.models import Token


User = get_user_model()


class TestToken(TestCase):

    def test_create_model(self):
        user = User.objects.create_user('user', 'user@email.com', '123456')
        token = Token.objects.create(user=user)
        self.assertEqual(smart_text(token), token.key)
        self.assertEqual(len(token.key), 40)
