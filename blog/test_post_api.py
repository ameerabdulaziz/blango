from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from pytz import UTC
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models import Post


class PostApiTestCase(TestCase):

    def setUp(self):
        self.u1 = get_user_model().objects.create(email='ahmed@test.com', password='1955')
        self.u2 = get_user_model().objects.create(email='amal@test.com', password='1964')

        posts = [
            Post.objects.create(
                author=self.u1,
                published_at=timezone.now(),
                title="Post 1 Title",
                slug="post-1-slug",
                summary="Post 1 Summary",
                content="Post 1 Content",
            ),
            Post.objects.create(
                author=self.u2,
                published_at=timezone.now(),
                title="Post 2 Title",
                slug="post-2-slug",
                summary="Post 2 Summary",
                content="Post 2 Content",
            ),
        ]
        self.post_lookup = {post.id: post for post in posts}

        self.client = APIClient()
        token = Token.objects.create(user=self.u1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.path = '/api/v1/posts/'

    def test_post_list(self):
        response = self.client.get(self.path)
        posts_data = response.json()

        self.assertEqual(len(posts_data), 2)
        for post in posts_data:
            post_obj = self.post_lookup[post['id']]
            self.assertEqual(post['title'], post_obj.title)
            self.assertEqual(post['slug'], post_obj.slug)
            self.assertEqual(post["summary"], post_obj.summary)
            self.assertEqual(post["content"], post_obj.content)
            self.assertTrue(post["author"].endswith(f'/api/v1/users/{post_obj.author.email}/'))
            self.assertEqual(datetime.strptime(post["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC), post_obj.published_at)

    def test_unauthenticated_post_create(self):
        self.client.credentials()
        post_dict = {
            "title": "Test Post",
            "slug": "test-post-3",
            "summary": "Test Summary",
            "content": "Test Content",
            "author": f"http://testserver/api/v1/users/{self.u1.email}/",
            "published_at": "2021-01-10T09:00:00Z",
        }
        response = self.client.post(self.path, post_dict)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Post.objects.count(), 2)

    def test_post_create(self):
        post_dict = {
            "title": "Test Post",
            "slug": "test-post-3",
            "summary": "Test Summary",
            "content": "Test Content",
            "author": f"http://testserver/api/v1/users/{self.u1.email}/",
            "published_at": "2021-01-10T09:00:00Z",
        }
        response = self.client.post(self.path, post_dict)
        print(response)
        print(response.json())
        post = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 3)

        post_obj = Post.objects.get(pk=post['id'])
        self.assertEqual(post['title'], post_obj.title)
        self.assertEqual(post['slug'], post_obj.slug)
        self.assertEqual(post["summary"], post_obj.summary)
        self.assertEqual(post["content"], post_obj.content)
        self.assertTrue(post["author"].endswith(f'/api/v1/users/{post_obj.author.email}/'))
        self.assertEqual(datetime(2021, 1, 10, 9, 0, 0, tzinfo=UTC), post_obj.published_at)
