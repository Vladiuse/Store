from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from user_api.models import Profile, Employee, Position
from faker import Faker

f = Faker()

User = get_user_model()

def create_user():
    return User.objects.create_user(username=f.first_name(), password='0000')

def create_employee_user():
    user = User.objects.create_user(username=f.first_name(), password='0000')
    position = Position.objects.create(id=f.first_name(), name=f.first_name())
    employee = Employee.objects.create(position=position, user=user)
    return employee, user

class UserTestCase(APITestCase):

    def test_is_employee(self):
        employee, user = create_employee_user()
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
