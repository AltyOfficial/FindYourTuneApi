from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from api.serializers import InstrumentSerailizer, InstrumentCategorySerializer
from info.models import Instrument, InstrumentCategory, Post, Tag, Band, Invite, Request


User = get_user_model()


class PostModelTests(APITestCase):
    """Post Model Testing."""

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.tag = Tag.objects.create(
            title='test tag',
            color='#123456',
            slug='test_slug'
        )
        self.post_data = {
            'title': 'Test Title',
            'tags': [
                1
            ]
        }

    def setUp(self):
        self.author = APIClient()
        self.client = APIClient()

        self.author_user = User.objects.create_superuser(
            'admin',
            'admin@admin.com',
            'admin123'
        )
        self.client_user = User.objects.create_user(
            'user',
            'user@user.com',
            'user1234'
        )

    def test_create_post(self):
        """Creating Post by authenticated user."""

        self.author.force_authenticate(user=self.author_user)

        post_count = Post.objects.count()

        url = '/api/posts/'
        response = self.author.post(url, self.post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), post_count + 1)

        response = self.client.post(url, self.post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post(self):
        """Updating Post by Author and Different User."""

        self.author.force_authenticate(user=self.author_user)
        self.client.force_authenticate(user=self.client_user)

        url = '/api/posts/'
        response = self.author.post(url, self.post_data, format='json')
        post_id = response.data.get('id')

        url = f'/api/posts/{post_id}/'
        response = self.author.patch(url, {'title': 'Updated Title'})

        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['id'], post_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(url, {'title': 'permission test'})

        self.assertEqual(Post.objects.get(id=post_id).title, 'Updated Title')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_post(self):
        """Deleting Post by Author and Different User."""

        self.author.force_authenticate(user=self.author_user)
        self.client.force_authenticate(user=self.client_user)

        url = '/api/posts/'
        response = self.author.post(url, self.post_data, format='json')
        post_id = response.data.get('id')

        post_count = Post.objects.count()

        url = f'/api/posts/{post_id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), post_count)

        response = self.author.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), post_count - 1)


class BandModelTests(APITestCase):
    """Post Model Testing."""

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.instrument_category = InstrumentCategory.objects.create(
            title='Strings',
            slug='strings'
        )
        self.instrument = Instrument.objects.create(
            title='Violin',
            category=self.instrument_category
        )
        self.band_data = {
            "title": "Test Title",
            "description": "test",
            "quantity": 5,
            "poster": ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"
                       "AgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA"
                       "7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5E"
                       "rkJggg=="),
            "your_instrument": "Violin"
        }

    def setUp(self):
        self.author = APIClient()
        self.client = APIClient()

        self.author_user = User.objects.create_superuser(
            'admin',
            'admin@admin.com',
            'admin123'
        )
        self.client_user = User.objects.create_user(
            'user',
            'user@user.com',
            'user1234'
        )
    
    def test_create_band(self):
        self.author.force_authenticate(user=self.author_user)

        band_count = Band.objects.count()

        url = '/api/bands/'
        response = self.author.post(url, self.band_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Band.objects.count(), band_count + 1)

        response = self.client.post(url, self.band_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_band(self):
        """Updating the Band."""

        self.author.force_authenticate(user=self.author_user)
        self.client.force_authenticate(user=self.client_user)

        url = '/api/bands/'
        response = self.author.post(url, self.band_data, format='json')
        band_id = response.data.get('id')

        url = f'/api/bands/{band_id}/'
        post_update_data = {
            'title': 'Updated Title'
        }
        response = self.author.patch(url, post_update_data)

        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['id'], band_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(url, {'title': 'permission test'})

        self.assertEqual(Band.objects.get(id=band_id).title, 'Updated Title')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_band_request(self):
        """Sending and Accepting Band Requests."""

        self.author.force_authenticate(user=self.author_user)

        url = '/api/bands/'
        response = self.author.post(url, self.band_data, format='json')
        band_id = response.data.get('id')
        band = Band.objects.get(id=band_id)

        url = f'/api/bands/{band_id}/send_request/'
        request_data = {'instrument': 'Violin'}
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.client_user)

        request_count = Request.objects.count()

        response = self.client.post(url, request_data, format='json')
        request_id = response.data.get('id')

        self.assertEqual(Request.objects.count(), request_count + 1)

        response = self.author.get('/api/requests/')

        self.assertEqual(response.data.get('count'), request_count + 1)
        self.assertEqual(band.participants.count(), 1)

        url = f'/api/requests/{request_id}/accept/'
        response = self.author.post(url)

        self.assertEqual(Request.objects.count(), request_count)
        self.assertEqual(band.participants.count(), 2)

        # Second request shall not work
        url = f'/api/bands/{band_id}/send_request/'
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_band_invite(self):
        """Sending and Accepting Invite to the Band."""

        self.author.force_authenticate(user=self.author_user)
        self.client.force_authenticate(user=self.client_user)

        url = '/api/bands/'
        response = self.author.post(url, self.band_data, format='json')
        band_id = response.data.get('id')
        band = Band.objects.get(id=band_id)
        client_id = self.client_user.id

        invite_count = Invite.objects.count()

        url = f'/api/users/{client_id}/invite_user/'
        invite_data = {'instrument': 'Violin'}
        response = self.author.post(url, invite_data, format='json')
        invite_id = response.data.get('id')

        self.assertEqual(Invite.objects.count(), invite_count + 1)

        url = f'/api/invites/{invite_id}/accept/'
        response = self.client.post(url)

        self.assertEqual(band.participants.count(), 2)


class InstrumentTagModelTesting(APITestCase):
    """Testing for Instrument and Tag Model."""

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.instrument_category = InstrumentCategory.objects.create(
            title='Strings',
            slug='strings'
        )
    
    def setUp(self):
        self.client = APIClient()
        self.client_user = User.objects.create_user(
            'user',
            'user@user.com',
            'user1234'
        )
    
    def test_cannot_create_instrument(self):
        """Instrument can be created only by Admin."""

        self.client.force_authenticate(user=self.client_user)

        url = '/api/instruments/'
        instrument_data = {
            'title': 'Cello',
            'category': 1
        }
        response = self.client.post(url, instrument_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_tag(self):
        """Tag can be created only by Admin."""

        self.client.force_authenticate(user=self.client_user)

        url = '/api/tags/'
        tag_data = {
            'title': 'Test Tag',
            'color': '#123456',
            'slug': 'testslug'
        }
        response = self.client.post(url, tag_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
