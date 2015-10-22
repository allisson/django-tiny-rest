# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from tiny_rest.models import Token


User = get_user_model()


class TestTokenAdmin(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'user', 'user@email.com', '123456'
        )
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username='user', password='123456')

    def test_list(self):
        Token.objects.create(user=self.user)
        response = self.client.get(
            reverse('admin:tiny_rest_token_changelist')
        )
        self.assertEqual(response.status_code, 200)
