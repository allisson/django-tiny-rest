# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from tiny_rest.models import Token


class TokenAdmin(admin.ModelAdmin):

    list_display = ('key', 'user', 'created_at', 'updated_at')
    search_fields = ['user__username', 'user__email', 'key']
    date_hierarchy = 'created_at'
    exclude = ('key', )


admin.site.register(Token, TokenAdmin)
