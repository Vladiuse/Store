from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from user_api.models import Profile, Employee, Position

User = get_user_model()


class UserTestCase(APITestCase):

    def test_is_employee(self):
        user = User.objects.create_user(username='test', password='0000')
        position = Position.objects.create(id='xxx', name='xxx')
        employee = Employee.objects.create(position=position, user=user)
        self.assertTrue(user.is_employee)

    def test_is_not_employee(self):
        user = User.objects.create_user(username='test', password='0000')
        self.assertFalse(user.is_employee)

class UserProfileTestCase(APITestCase):


    def test_create_user_with_profile(self):
        User.objects.create_user(username='vlad', password='0000')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_delete_profile_with_user(self):
        user = User.objects.create_user(username='vlad', password='0000')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        user.delete()
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
