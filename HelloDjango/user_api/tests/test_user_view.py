from django.test import TestCase
import unittest
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from user_api.models import Profile, Employee, Position
from .test_user_model import create_employee_user, create_user

User = get_user_model()


class UserView(APITestCase):

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


class UserViewList(APITestCase):
    def test_get_users_list_not_auth(self):
        user_list_url = reverse('myuser-list')
        res = self.client.get(user_list_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_list_not_employee(self):
        user = create_user()
        self.client.force_login(user=user)
        user_list_url = reverse('myuser-list')
        res = self.client.get(user_list_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_list_employee_user(self):
        employee, user = create_employee_user()
        self.client.force_login(user=user)
        user_list_url = reverse('myuser-list')
        res = self.client.get(user_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class UserViewDetail(APITestCase):

    def test_not_auth(self):
        user = create_user()
        user_detail_url = reverse('myuser-detail', args=[user.pk, ])
        res = self.client.get(user_detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_auth_not_employee(self):
        user = create_user()
        self.client.force_login(user=user)
        user_detail_url = reverse('myuser-detail', args=[user.pk, ])
        res = self.client.get(user_detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_employee_show_self(self):
        employee, user = create_employee_user()
        self.client.force_login(user=user)
        user_detail_url = reverse('myuser-detail', args=[user.pk, ])
        res = self.client.get(user_detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_employee_other_user_detail(self):
        employee, user = create_employee_user()
        user_1 = create_user()
        self.client.force_login(user=user)
        user_detail_url = reverse('myuser-detail', args=[user_1.pk, ])
        res = self.client.get(user_detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
