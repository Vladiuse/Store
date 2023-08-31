from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from user_api.models import Profile, Employee, Position, UserAddress
from faker import Faker
from ..test_user_model import create_user, create_employee_user

f = Faker()

User = get_user_model()


class UserAddressViewGetTest(APITestCase):

    def test_no_auth_user(self):
        user = create_user()
        address = UserAddress.objects.create(owner=user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_own_address(self):
        user = create_user()
        address = UserAddress.objects.create(owner=user, address=f.address())
        self.client.force_login(user=user)
        url = reverse('useraddress-detail', args=[address.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_foreign_user_address(self):
        user = create_user()
        foreign_user = create_user()
        address = UserAddress.objects.create(owner=foreign_user, address=f.address())
        self.client.force_login(user=user)
        url = reverse('useraddress-detail', args=[address.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_see_user_address(self):
        employee, user = create_employee_user()
        self.client.force_login(user=user)
        user = create_user()
        address = UserAddress.objects.create(owner=user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class UserAddressViewList(APITestCase):

    def test_no_auth_user(self):
        url = reverse('useraddress-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user(self):
        user = create_user()
        self.client.force_login(user=user)
        url = reverse('useraddress-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        url = reverse('useraddress-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class UserAddressViewCreate(APITestCase):

    def test_no_auth_user(self):
        url = reverse('useraddress-list')
        res = self.client.post(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user(self):
        user = create_user()
        self.client.force_login(user=user)
        url = reverse('useraddress-list')
        data = {
            'address': f.address()
        }
        res = self.client.post(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.addresses.count(), 1)


class UserAddressViewUpdate(APITestCase):

    def test_no_auth_user(self):
        user = create_user()
        address = UserAddress.objects.create(owner=user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        data = {
            'address': f.address()
        }
        res = self.client.put(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_foreign_address(self):
        user = create_user()
        self.client.force_login(user=user)
        foreign_user = create_user()
        address = UserAddress.objects.create(owner=foreign_user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        data = {
            'address': f.address()
        }
        res = self.client.put(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_own_address(self):
        user = create_user()
        self.client.force_login(user=user)
        address = UserAddress.objects.create(owner=user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        data = {
            'address': f.address()
        }
        res = self.client.put(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.patch(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_employee_update_user_address(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        user = create_user()
        address = UserAddress.objects.create(owner=user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        data = {
            'address': f.address()
        }

        res = self.client.put(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class UserAddressViewDelete(APITestCase):

    def test_no_auth_user(self):
        user = create_user()
        address = UserAddress.objects.create(owner=user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_own_address(self):
        user = create_user()
        self.client.force_login(user=user)
        address = UserAddress.objects.create(owner=user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_foreign_address(self):
        user = create_user()
        self.client.force_login(user=user)
        foreign_user = create_user()
        address = UserAddress.objects.create(owner=foreign_user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_foreign_address(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        foreign_user = create_user()
        address = UserAddress.objects.create(owner=foreign_user, address=f.address())
        url = reverse('useraddress-detail', args=[address.pk, ])
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)



