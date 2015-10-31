# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

import json
import status

from tiny_rest.views import APIView
from tiny_rest.pagination import PaginationMixin


class PaginationAPIView(PaginationMixin, APIView):

    paginate_by = 5

    def list(self, request, *args, **kwargs):
        objects = range(10)
        object_list, pagination = self.paginate_objects(request, objects)
        data = {
            'pagination': pagination,
            'data': [number for number in object_list]
        }
        return self.response(data=data)


class TestPaginationAPIView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_paginate_objects(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = PaginationAPIView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content.decode())
        self.assertEqual(data['pagination']['count'], 10)
        self.assertEqual(data['pagination']['num_pages'], 2)
        self.assertFalse(data['pagination']['previous_page_number'])
        self.assertFalse(data['pagination']['previous_url'])
        self.assertEqual(data['pagination']['next_page_number'], 2)
        self.assertEqual(
            data['pagination']['next_url'], 'http://testserver/?page=2'
        )
        self.assertEqual(data['data'], [0, 1, 2, 3, 4])

        request = self.factory.get('/?page=2')
        request.user = AnonymousUser()
        response = PaginationAPIView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content.decode())
        self.assertEqual(data['pagination']['count'], 10)
        self.assertEqual(data['pagination']['num_pages'], 2)
        self.assertEqual(data['pagination']['previous_page_number'], 1)
        self.assertEqual(
            data['pagination']['previous_url'], 'http://testserver/?page=1'
        )
        self.assertFalse(data['pagination']['next_page_number'])
        self.assertFalse(data['pagination']['next_url'])
        self.assertEqual(data['data'], [5, 6, 7, 8, 9])
