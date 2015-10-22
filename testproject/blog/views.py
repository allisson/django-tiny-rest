# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tiny_rest.views import APIView
from tiny_rest.authorization import IsAuthenticatedOrReadOnlyMixin
import status

from blog.models import Post, Comment, post_to_dict, comment_to_dict
from blog.forms import PostForm


class PostAPIView(IsAuthenticatedOrReadOnlyMixin, APIView):

    def get_post(self):
        try:
            return Post.objects.get(pk=self.pk)
        except Post.DoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(published=True)
        object_list, pagination = self.paginate_objects(request, queryset)

        data = {
            'pagination': pagination,
            'data': [post_to_dict(request, post) for post in object_list]
        }
        return self.response(data=data)

    def detail(self, request, *args, **kwargs):
        post = self.get_post()
        if not post:
            return self.resource_not_found()

        return self.response(data=post_to_dict(request, post))

    def create(self, request, *args, **kwargs):
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save()
            return self.response(
                data=post_to_dict(request, post),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return self.response(
                data={'error': form.errors},
                status_code=status.HTTP_400_BAD_REQUEST
            )


class CommentAPIView(IsAuthenticatedOrReadOnlyMixin, APIView):

    def load_post(self):
        try:
            return Post.objects.get(pk=self.kwargs.get('post_pk'))
        except Post.DoesNotExist:
            return None

    def get_comment(self, post):
        try:
            return Comment.objects.get(post=post, pk=self.pk)
        except Comment.DoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        post = self.load_post()
        if not post:
            return self.resource_not_found()

        queryset = Comment.objects.filter(post=post)
        object_list, pagination = self.paginate_objects(request, queryset)

        data = {
            'pagination': pagination,
            'data': [
                comment_to_dict(request, comment) for comment in object_list
            ]
        }

        return self.response(data=data)

    def detail(self, request, *args, **kwargs):
        post = self.load_post()
        if not post:
            return self.resource_not_found()

        comment = self.get_comment(post)
        if not comment:
            return self.resource_not_found()

        return self.response(data=comment_to_dict(request, comment))


# cbv -> fbv
post_api = PostAPIView.as_view()
comment_api = CommentAPIView.as_view()
