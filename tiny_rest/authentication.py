# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate

import base64


class BasicAuthMixin(object):

    def authenticate(self, request):
        request.user = AnonymousUser()

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()

            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    username, password = base64.b64decode(auth[1]).split(':')
                    user = authenticate(username=username, password=password)
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
