# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns(
    '',
    # admin
    url(r'^admin/', include(admin.site.urls)),

    # blog
    url(r'^', include('blog.urls')),
)
