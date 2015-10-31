# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms.models import model_to_dict

from tiny_rest.views import APIView
from tiny_rest.authorization import IsAuthenticatedOrReadOnlyMixin
from tiny_rest.pagination import PaginationMixin
import status

from blog.models import Post, Comment, post_to_dict, comment_to_dict
from blog.forms import PostForm, CommentForm


class PostAPIView(IsAuthenticatedOrReadOnlyMixin, PaginationMixin, APIView):

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
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return self.response(
                data=post_to_dict(request, post),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return self.response(
                data={'error': form.errors},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        post = self.get_post()
        if not post:
            return self.resource_not_found()

        form = PostForm(data=request.PUT, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return self.response(
                data=post_to_dict(request, post),
                status_code=status.HTTP_200_OK
            )
        else:
            return self.response(
                data={'error': form.errors},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, *args, **kwargs):
        post = self.get_post()
        if not post:
            return self.resource_not_found()

        data = model_to_dict(post)
        data.update(request.PATCH.dict())
        form = PostForm(data=data, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return self.response(
                data=post_to_dict(request, post),
                status_code=status.HTTP_200_OK
            )
        else:
            return self.response(
                data={'error': form.errors},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        post = self.get_post()
        if not post:
            return self.resource_not_found()

        post.delete()
        return self.response(data={}, status_code=status.HTTP_204_NO_CONTENT)


class CommentAPIView(IsAuthenticatedOrReadOnlyMixin, PaginationMixin, APIView):

    paginate_by = 10

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

    def create(self, request, *args, **kwargs):
        post = self.load_post()
        if not post:
            return self.resource_not_found()

        form = CommentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return self.response(
                data=comment_to_dict(request, comment),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return self.response(
                data={'error': form.errors},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        post = self.load_post()
        if not post:
            return self.resource_not_found()

        comment = self.get_comment(post)
        if not comment:
            return self.resource_not_found()

        form = CommentForm(
            data=request.PUT, files=request.FILES, instance=comment
        )
        if form.is_valid():
            comment = form.save()
            return self.response(
                data=comment_to_dict(request, comment),
                status_code=status.HTTP_200_OK
            )
        else:
            return self.response(
                data={'error': form.errors},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, *args, **kwargs):
        post = self.load_post()
        if not post:
            return self.resource_not_found()

        comment = self.get_comment(post)
        if not comment:
            return self.resource_not_found()

        data = model_to_dict(comment)
        data.update(request.PATCH.dict())
        form = CommentForm(data=data, files=request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save()
            return self.response(
                data=comment_to_dict(request, comment),
                status_code=status.HTTP_200_OK
            )
        else:
            return self.response(
                data={'error': form.errors},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        post = self.load_post()
        if not post:
            return self.resource_not_found()

        comment = self.get_comment(post)
        if not comment:
            return self.resource_not_found()

        comment.delete()
        return self.response(data={}, status_code=status.HTTP_204_NO_CONTENT)


# cbv -> fbv
post_api = PostAPIView.as_view()
comment_api = CommentAPIView.as_view()
