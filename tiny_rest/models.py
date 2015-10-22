# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.crypto import get_random_string


@python_2_unicode_compatible
class Token(models.Model):

    key = models.CharField(
        _('key'),
        max_length=40,
        primary_key=True,
        default=get_random_string(40)
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='auth_token_list'
    )

    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'tokens'
        ordering = ['-created_at']
