# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'blog.views',
    url(
        r'^api/posts/$', 'post_api', name='post_api'
    ),
    url(
        r'^api/posts/(?P<pk>\d+)/$', 'post_api', name='post_api'
    ),
    url(
        r'^api/posts/(?P<post_pk>\d+)/comments/$', 'comment_api',
        name='comment_api'
    ),
    url(
        r'^api/posts/(?P<post_pk>\d+)/comments/(?P<pk>\d+)/$', 'comment_api',
        name='comment_api'
    ),
)
