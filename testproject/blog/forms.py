# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('user', )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', )
