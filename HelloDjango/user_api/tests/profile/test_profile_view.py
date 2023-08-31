import unittest

from rest_framework.test import APITestCase
from user_api.models import Profile
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework import status
from ..test_user_model import create_user, create_employee_user


User = get_user_model()


class ProfileViewCreateTest(APITestCase):

    def test_protect_create_no_auth(self):
        url = reverse('profile-list')
        res = self.client.post(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_protect_profile_create_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        url = reverse('profile-list')
        res = self.client.post(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ProfileViewDeleteTest(APITestCase):

    def test_protect_delete_no_auth(self):
        user = create_user()
        url = reverse('profile-detail', args=[user.profile.pk, ])
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_protect_delete_not_employee(self):
        user = create_user()
        self.client.force_login(user=user)
        url = reverse('profile-detail', args=[user.profile.pk, ])
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_protect_delete_employee(self):
        user = create_user()
        employee, emp_user = create_employee_user()
        url = reverse('profile-detail', args=[user.profile.pk,])
        self.client.force_login(user=emp_user)
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class ProfileViewGetTest(APITestCase):

    def test_see_profile_no_auth(self):
        user = create_user()
        url = reverse('profile-detail', args=[user.profile.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_see_profile_auth_own_profile(self):
        user = create_user()
        self.client.force_login(user=user)
        url = reverse('profile-detail', args=[user.profile.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_see_foreign_profile_not_empoyee(self):
        foreign_user = create_user()
        user = create_user()
        self.client.force_login(user=user)
        url = reverse('profile-detail', args=[foreign_user.profile.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_see_profile_by_employee(self):
        user = create_user()
        employee, emp_user = create_employee_user()
        url = reverse('profile-detail', args=[user.profile.pk, ])
        self.client.force_login(user=emp_user)
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

class ProfileViewUpdateTest(APITestCase):

    def test_no_auth_user(self):
        user = create_user()
        url = reverse('profile-detail', args=[user.profile.pk, ])
        res = self.client.put(url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.patch(url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_user(self):
        user = create_user()
        url = reverse('profile-detail', args=[user.profile.pk, ])
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.put(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.patch(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_foreign_profile_user(self):
        user = create_user()
        url = reverse('profile-detail', args=[user.profile.pk, ])
        foreign_user = create_user()
        self.client.force_login(user=foreign_user)
        res = self.client.put(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.patch(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_own_profile_update(self):
        user = create_user()
        url = reverse('profile-detail', args=[user.profile.pk, ])
        self.client.force_login(user=user)
        data = {
            'owner': user.pk,
            'first_name': 'xxx',
            'last_name': 'xxx',
            'sex': Profile.MAN,
            'age': 20,
        }
        res = self.client.put(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_own_profile_update_partial(self):
        user = create_user()
        url = reverse('profile-detail', args=[user.profile.pk, ])
        self.client.force_login(user=user)
        data = {
            # 'owner': user.pk,
            # 'first_name': 'xxx',
            # 'last_name': 'xxx',
            # 'sex': Profile.MAN,
            'age': 20,
        }
        res = self.client.patch(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


