# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from blog.models import Post, Comment


class PostAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'slug', 'user', 'published', 'created_at', 'updated_at'
    )
    list_filter = ('user', 'published')
    search_fields = ['title', 'body']
    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):

    list_display = ('user', 'post', 'created_at', 'updated_at')
    list_filter = ('user', 'post',)
    search_fields = ['comment', ]
    date_hierarchy = 'created_at'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
