# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate

import base64


class BasicAuthMixin(object):

    def authenticate(self, request):
        request.user = AnonymousUser()

        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth:
            auth = auth.split()

            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    u, p = base64.b64decode(auth[1]).decode().split(':')
                    user = authenticate(username=u, password=p)
                    if user:
                        if user.is_active:
                            request.user = user


class TokenAuthMixin(object):

    def authenticate(self, request):
        request.user = AnonymousUser()
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if len(auth_header.split(' ')) == 2:
            token = auth_header.split(' ')[1]
            user = authenticate(token=token)
            if user:
                if user.is_active:
                    request.user = user
