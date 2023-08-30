import unittest

from rest_framework.test import APITestCase
from user_api.models import Profile
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework import status


User = get_user_model()

class ProfileTestCase(APITestCase):


    def test_block_delete_of_profile(self):
        user = User.objects.create_user(username='vlad', password='0000')
        profile = user.profile
        self.assertRaises(NotImplementedError, profile.delete)

    @unittest.skip('can be createt bu Anonimus user')
    def test_creation_not_allowed(self):
        profile_url = reverse('profile-list')
        res = self.client.post(profile_url, data={})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)