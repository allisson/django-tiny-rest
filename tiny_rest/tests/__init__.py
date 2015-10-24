# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test.client import (
    RequestFactory as DjangoRequestFactory, Client as DjangoClient,
    MULTIPART_CONTENT
)


class RequestFactory(DjangoRequestFactory):

    def put(self, path, data=None, content_type=MULTIPART_CONTENT,
            secure=False, **extra):
        "Construct a PUT request."

        data = {} if data is None else data
        post_data = self._encode_data(data, content_type)

        return self.generic('PUT', path, post_data, content_type,
                            secure=secure, **extra)

    def patch(self, path, data=None, content_type=MULTIPART_CONTENT,
              secure=False, **extra):
        "Construct a PATCH request."

        data = {} if data is None else data
        post_data = self._encode_data(data, content_type)

        return self.generic('PATCH', path, post_data, content_type,
                            secure=secure, **extra)


class Client(RequestFactory, DjangoClient):
    pass
