# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tiny_rest.constants import SAFE_METHODS


class IsAuthenticatedMixin(object):

    def authorize(self, request):
        return request.user.is_authenticated()


class IsAuthenticatedOrReadOnlyMixin(object):

    def authorize(self, request):
        if request.method not in SAFE_METHODS:
            if not request.user.is_authenticated():
                return False

        return True
