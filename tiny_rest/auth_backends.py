# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from tiny_rest.models import Token


User = get_user_model()


class TokenAuthBackend(ModelBackend):

    def authenticate(self, token=None):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None
