# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class CreateUpdateModel(models.Model):

    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Post(CreateUpdateModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='posts'
    )

    title = models.CharField(
        _('title'),
        max_length=100
    )

    slug = models.SlugField(
        _('slug'),
        max_length=100,
        unique=True
    )

    body = models.TextField(
        _('body')
    )

    published = models.BooleanField(
        _('published'),
        default=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Comment(CreateUpdateModel):

    post = models.ForeignKey(
        'Post',
        verbose_name=_('post'),
        related_name='comments'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='comments'
    )

    comment = models.TextField(
        _('comment'),
        max_length=2048
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.comment[:50])


def user_to_dict(request, user):
    return {
        'id': user.pk,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.get_full_name(),
        'date_joined': user.date_joined
    }


def post_to_dict(request, post):
    return {
        'id': post.pk,
        'user': user_to_dict(request, post.user),
        'title': post.title,
        'slug': post.slug,
        'body': post.body,
        'published': post.published,
        'created_at': post.created_at,
        'updated_at': post.updated_at
    }


def comment_to_dict(request, comment):
    return {
        'id': comment.pk,
        'post': comment.post.pk,
        'user': user_to_dict(request, comment.user),
        'comment': comment.comment,
        'created_at': comment.created_at,
        'updated_at': comment.updated_at
    }
