# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

import status

from tiny_rest.views import APIView


class TestAPIView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_method_not_allowed(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request, pk=1)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

        request = self.factory.post('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        request = self.factory.post('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request, pk=1)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

        request = self.factory.put('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        request = self.factory.put('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request, pk=1)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

        request = self.factory.patch('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        request = self.factory.patch('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request, pk=1)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

        request = self.factory.delete('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        request = self.factory.delete('/')
        request.user = AnonymousUser()
        response = APIView.as_view()(request, pk=1)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
