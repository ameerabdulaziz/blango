from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient

from blog.models import Tag


class TagApiTestCase(LiveServerTestCase):
    def setUp(self):
        get_user_model().objects.create_user(email='afnan@test.com', password='1994')

        self.tag_values = {'tag1', 'tag2', 'tag3'}
        for tag in self.tag_values:
            Tag.objects.create(value=tag)

        self.client = RequestsClient()
        self.path = '/api/v1/tags/'

    def test_tag_list(self):
        response = self.client.get(self.live_server_url + self.path)
        self.assertEqual(response.status_code, 200)

        tags_data = response.json()['results']
        self.assertEqual(len(tags_data), 3)
        self.assertEqual({tag['value'] for tag in tags_data}, self.tag_values)

    def test_tag_create_basic_auth(self):
        self.client.auth = HTTPBasicAuth('afnan@test.com', '1994')
        response = self.client.post(self.live_server_url + self.path, {'value': 'tag test'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), 4)

    def test_tag_create_token_auth(self):
        token_response = self.client.post(
            self.live_server_url + '/api/v1/token-auth/', {'username': 'afnan@test.com', 'password': '1994'}
        )
        self.client.headers['Authorization'] = f"Token {token_response.json()['token']}"
        response = self.client.post(self.live_server_url + self.path, {'value': 'tag test'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), 4)