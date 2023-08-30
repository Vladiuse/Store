from django.test import TestCase
import unittest
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from user_api.models import Profile, Employee, Position

User = get_user_model()


class UserViewTestCase(APITestCase):

    def setUp(self) -> None:
        #
        self.create_user()

    def create_user(self):
        User.objects.create_user(username='vlad', password='0000')

    def test_login_incorrect_username(self):
        login_url = reverse('login')
        data = {
            'username': 'vlad1',
            'password': '0000',
        }
        res = self.client.post(login_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_incorrect_password(self):
        login_url = reverse('login')
        data = {
            'username': 'vlad',
            'password': '00000000',
        }
        res = self.client.post(login_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_correct_log_pass(self):
        login_url = reverse('login')
        data = {
            'username': 'vlad',
            'password': '0000',
        }
        res = self.client.post(login_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], 'vlad')

    def test_logout(self):
        login_url = reverse('login')
        data = {
            'username': 'vlad',
            'password': '0000',
        }
        res = self.client.post(login_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_user_registration(self):
        register_url = reverse('register')
        data = {
            'username': 'some',
            'password': '0000',
        }
        res = self.client.post(register_url, data=data, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(User.objects.count(), 2)
