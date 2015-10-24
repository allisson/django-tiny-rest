# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

import json
from model_mommy import mommy
from io import BytesIO
from PIL import Image
from tiny_rest.tests import Client
import status

from blog.models import Post, Comment


User = get_user_model()


class TestPostAPIView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'user', 'user@email.com', '123456'
        )
        self.list_url = reverse('blog:post_api')
        self.posts = mommy.make(Post, user=self.user, _quantity=20)
        self.detail_url = reverse('blog:post_api', args=[self.posts[0].pk])
        self.file_obj = BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
        image.save(self.file_obj, 'PNG')
        self.file_obj.name = 'test.jpg'
        self.file_obj.seek(0)
        self.client.login(username='user', password='123456')

    def tearDown(self):
        for post in Post.objects.all():
            post.image.delete()
            post.delete()

    def test_list(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.list_url, {'page': 'invalid'})
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.list_url, {'page': 100})
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        data = json.loads(response.content.decode())
        self.assertEqual(data['id'], self.posts[0].pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.posts[0].delete()
        response = self.client.get(self.detail_url)
        data = json.loads(response.content.decode())
        self.assertEqual(data['error'], 'Resource Not Found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        response = self.client.post(self.list_url, {})
        data = json.loads(response.content.decode())
        self.assertEqual(data['error']['body'][0], 'This field is required.')
        self.assertEqual(data['error']['image'][0], 'This field is required.')
        self.assertEqual(data['error']['slug'][0], 'This field is required.')
        self.assertEqual(data['error']['title'][0], 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            self.list_url,
            {
                'title': 'my post',
                'slug': 'my-post',
                'body': 'my body',
                'image': self.file_obj
            }
        )
        data = json.loads(response.content.decode())
        self.assertEqual(data['title'], 'my post')
        self.assertEqual(data['slug'], 'my-post')
        self.assertEqual(data['body'], 'my body')
        self.assertEqual(data['user']['id'], self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        response = self.client.put(self.detail_url, {})
        data = json.loads(response.content.decode())
        self.assertEqual(data['error']['body'][0], 'This field is required.')
        self.assertEqual(data['error']['slug'][0], 'This field is required.')
        self.assertEqual(data['error']['title'][0], 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(
            self.detail_url,
            {
                'title': 'my post',
                'slug': 'my-post',
                'body': 'my body',
                'image': self.file_obj
            },
        )
        data = json.loads(response.content.decode())
        self.assertEqual(data['title'], 'my post')
        self.assertEqual(data['slug'], 'my-post')
        self.assertEqual(data['body'], 'my body')
        self.assertEqual(data['user']['id'], self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        post = self.posts[0]

        response = self.client.patch(
            self.detail_url,
            {
                'title': 'my post',
            },
        )
        data = json.loads(response.content.decode())
        self.assertEqual(data['title'], 'my post')
        self.assertEqual(data['slug'], post.slug)
        self.assertEqual(data['body'], post.body)
        self.assertEqual(data['user']['id'], post.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        post = self.posts[0]
        response = self.client.delete(self.detail_url)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(self.detail_url)
        data = json.loads(response.content.decode())
        self.assertEqual(data['error'], 'Resource Not Found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestCommentAPIView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'user', 'user@email.com', '123456'
        )
        self.post = mommy.make(Post, user=self.user)
        self.comments = mommy.make(
            Comment, post=self.post, user=self.user, _quantity=20
        )
        self.list_url = reverse('blog:comment_api', args=[self.post.pk])
        self.detail_url = reverse(
            'blog:comment_api', args=[self.post.pk, self.comments[0].pk]
        )
        self.client.login(username='user', password='123456')

    def test_list(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.list_url, {'page': 'invalid'})
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.list_url, {'page': 100})
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        data = json.loads(response.content.decode())
        self.assertEqual(data['id'], self.comments[0].pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.comments[0].delete()
        response = self.client.get(self.detail_url)
        data = json.loads(response.content.decode())
        self.assertEqual(data['error'], 'Resource Not Found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        response = self.client.post(self.list_url, {})
        data = json.loads(response.content.decode())
        self.assertEqual(
            data['error']['comment'][0], 'This field is required.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            self.list_url,
            {
                'comment': 'my comment'
            }
        )
        data = json.loads(response.content.decode())
        self.assertEqual(data['post'], self.post.pk)
        self.assertEqual(data['comment'], 'my comment')
        self.assertEqual(data['user']['id'], self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        response = self.client.put(self.detail_url, {})
        data = json.loads(response.content.decode())
        self.assertEqual(
            data['error']['comment'][0], 'This field is required.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(
            self.detail_url,
            {
                'comment': 'my comment'
            },
        )
        data = json.loads(response.content.decode())
        self.assertEqual(data['post'], self.post.pk)
        self.assertEqual(data['comment'], 'my comment')
        self.assertEqual(data['user']['id'], self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        comment = self.comments[0]

        response = self.client.patch(
            self.detail_url,
            {
                'comment': 'my comment',
            },
        )
        data = json.loads(response.content.decode())
        self.assertEqual(data['id'], comment.pk)
        self.assertEqual(data['post'], self.post.pk)
        self.assertEqual(data['comment'], 'my comment')
        self.assertEqual(data['user']['id'], self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        comment = self.comments[0]
        response = self.client.delete(self.detail_url)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(self.detail_url)
        data = json.loads(response.content.decode())
        self.assertEqual(data['error'], 'Resource Not Found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
