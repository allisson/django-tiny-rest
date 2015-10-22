# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import AnonymousUser

import json
import status

from tiny_rest.views import APIView
from tiny_rest.authorization import (
    IsAuthenticatedMixin, IsAuthenticatedOrReadOnlyMixin
)


User = get_user_model()


class IsAuthenticatedAPIView(IsAuthenticatedMixin, APIView):

    def list(self, request, *args, **kwargs):
        return self.response(
            data={'is_authenticated': request.user.is_authenticated()}
        )


class IsAuthenticatedOrReadOnlyAPIView(IsAuthenticatedOrReadOnlyMixin,
                                       APIView):

    def list(self, request, *args, **kwargs):
        return self.response(
            data={'is_authenticated': request.user.is_authenticated()}
        )

    def create(self, request, *args, **kwargs):
        return self.response(
            data={'is_authenticated': request.user.is_authenticated()}
        )


class BaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            'user', 'user@email.com', '123456'
        )


class TestIsAuthenticatedAPIView(BaseTestCase):

    def test_authenticate(self):
        request = self.factory.get('/')
        request.user = authenticate(username='user', password='123456')
        response = IsAuthenticatedAPIView.as_view()(request)
        data = json.loads(response.content)
        self.assertTrue(data['is_authenticated'])

        request.user = AnonymousUser()
        response = IsAuthenticatedAPIView.as_view()(request)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Not Authorized')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestIsAuthenticatedOrReadOnlyAPIView(BaseTestCase):

    def test_authenticate(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = IsAuthenticatedOrReadOnlyAPIView.as_view()(request)
        data = json.loads(response.content)
        self.assertFalse(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = self.factory.post('/')
        request.user = AnonymousUser()
        response = IsAuthenticatedOrReadOnlyAPIView.as_view()(request)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Not Authorized')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = self.factory.get('/')
        request.user = authenticate(username='user', password='123456')
        response = IsAuthenticatedOrReadOnlyAPIView.as_view()(request)
        data = json.loads(response.content)
        self.assertTrue(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = self.factory.post('/')
        request.user = authenticate(username='user', password='123456')
        response = IsAuthenticatedOrReadOnlyAPIView.as_view()(request)
        data = json.loads(response.content)
        self.assertTrue(data['is_authenticated'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
