# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from django.utils.timezone import make_aware, get_default_timezone
from django.contrib.auth.models import AnonymousUser

from datetime import datetime
from decimal import Decimal
from uuid import uuid4
import json

from tiny_rest.http import DjangoJSONEncoder
from tiny_rest.views import APIView


class TestDjangoJSONEncoder(TestCase):

    def setUp(self):
        self.encoder = DjangoJSONEncoder

    def test_json_dumps(self):
        with self.assertRaises(ValueError):
            json.dumps(
                {
                    'date': datetime.now().date(),
                    'time': make_aware(
                        datetime.now().time(), get_default_timezone()
                    ),
                    'datetime': datetime.now(),
                    'decimal': Decimal('100.00'),
                    'uuid4': uuid4()
                },
                cls=self.encoder
            )

        data = json.dumps(
            {
                'date': datetime.now().date(),
                'time': datetime.now().time(),
                'datetime': datetime.now(),
                'decimal': Decimal('100.00'),
                'uuid4': uuid4()
            },
            cls=self.encoder
        )
        self.assertIn('date', data)
        self.assertIn('time', data)
        self.assertIn('datetime', data)
        self.assertIn('decimal', data)
        self.assertIn('uuid4', data)


class JsonResponseAPIView(APIView):

    def list(self, request, *args, **kwargs):
        return self.response(data=[{'name': 'Allisson'}])


class TestJsonResponseAPIView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_json_response_exception(self):
        with self.assertRaises(TypeError):
            request = self.factory.get('/')
            request.user = AnonymousUser()
            JsonResponseAPIView.as_view()(request)
