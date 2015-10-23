# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

import json
import base64
import status

from tiny_rest.models import Token
from tiny_rest.views import APIView
from tiny_rest.authentication import BasicAuthMixin, TokenAuthMixin


User = get_user_model()


class SessionAPIView(APIView):

    def list(self, request, *args, **kwargs):
        return self.response(
            data={'is_authenticated': request.user.is_authenticated()}
        )


class BasicAuthAPIView(BasicAuthMixin, APIView):

    def list(self, request, *args, **kwargs):
        return self.response(
            data={'is_authenticated': request.user.is_authenticated()}
        )


class TokenAuthAPIView(TokenAuthMixin, APIView):

    def list(self, request, *args, **kwargs):
        return self.response(
            data={'is_authenticated': request.user.is_authenticated()}
        )


class BaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            'user', 'user@email.com', '123456'
        )


class TestSessionAPIView(BaseTestCase):

    def test_authenticate(self):
        request = self.factory.get('/')
        request.user = authenticate(username='user', password='123456')
        response = SessionAPIView.as_view()(request)
        data = json.loads(response.content.decode())
        self.assertTrue(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.is_active = False
        self.user.save()
        request.user = authenticate(username='user', password='123456')
        response = SessionAPIView.as_view()(request)
        data = json.loads(response.content.decode())
        self.assertFalse(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBasicAuthAPIView(BaseTestCase):

    def test_authenticate(self):
        request = self.factory.get('/')

        basic_auth = '{0}:{1}'.format('user', '123456')
        request.META['HTTP_AUTHORIZATION'] = 'Basic {0}'.format(
            base64.b64encode(basic_auth.encode()).decode()
        )
        response = BasicAuthAPIView.as_view()(request)
        data = json.loads(response.content.decode())
        self.assertTrue(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        basic_auth = '{0}:{1}'.format('user', '1234567')
        request.META['HTTP_AUTHORIZATION'] = 'Basic {0}'.format(
            base64.b64encode(basic_auth.encode()).decode()
        )
        response = BasicAuthAPIView.as_view()(request)
        data = json.loads(response.content.decode())
        self.assertFalse(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        basic_auth = '{0}:{1}'.format('user', '123456')
        request.META['HTTP_AUTHORIZATION'] = 'Basic {0}'.format(
            base64.b64encode(basic_auth.encode()).decode()
        )
        self.user.is_active = False
        self.user.save()
        response = BasicAuthAPIView.as_view()(request)
        data = json.loads(response.content.decode())
        self.assertFalse(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTokenAuthAPIView(BaseTestCase):

    def test_authenticate(self):
        request = self.factory.get('/')
        token = Token.objects.create(user=self.user)

        request.META['HTTP_AUTHORIZATION'] = 'Token {0}'.format(token.key)
        response = TokenAuthAPIView.as_view()(request)
        data = json.loads(response.content.decode())
        self.assertTrue(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request.META['HTTP_AUTHORIZATION'] = 'Token {0}'.format('invalid-key')
        response = TokenAuthAPIView.as_view()(request)
        data = json.loads(response.content.decode())
        self.assertFalse(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.is_active = False
        self.user.save()
        request.META['HTTP_AUTHORIZATION'] = 'Token {0}'.format(token.key)
        response = TokenAuthAPIView.as_view()(request)
        data = json.loads(response.content.decode())
        self.assertFalse(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
