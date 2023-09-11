from store.models import BannerAdd
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from django.contrib.auth.models import Group
from _helptools import create_banner, create_user, create_employee_user, banner_fake_data


class BannerAddViewRetrieveTest(APITestCase):

    def setUp(self) -> None:
        self.banner = create_banner()
        self.banner_url = reverse('banners-detail', args=[self.banner.pk, ])

    def test_no_auth(self):
        res = self.client.get(self.banner_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.banner_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class BannerAddViewListTest(APITestCase):

    def setUp(self) -> None:
        self.banner = create_banner()
        self.banner_url = reverse('banners-list')

    def test_no_auth(self):
        res = self.client.get(self.banner_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.banner_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)


class BannerAddViewCreateTest(APITestCase):

    def setUp(self) -> None:
        self.banner_url = reverse('banners-list')

        Group.objects.create(name='moderator')

    def test_no_auth(self):
        res = self.client.post(self.banner_url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.post(self.banner_url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_employee(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        data = banner_fake_data(json=True)
        res = self.client.post(self.banner_url, data=data, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_employee_moderator(self):
        employee, emp_moderator = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_moderator)
        data = banner_fake_data(json=True, order=1)
        res = self.client.post(self.banner_url, data=data, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_few_banners(self):
        employee, emp_moderator = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_moderator)
        for _ in range(3):
            data = banner_fake_data(json=True, order=1)
            res = self.client.post(self.banner_url, data=data, format='multipart')
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BannerAdd.objects.count(), 3)


class BannerAddViewUpdateTest(APITestCase):

    def setUp(self) -> None:
        self.banner = create_banner()
        self.banner_url = reverse('banners-detail', args=[self.banner.pk, ])

        Group.objects.create(name='moderator')

    def test_no_auth(self):
        res = self.client.put(self.banner_url, data={}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(self.banner_url, data={}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.put(self.banner_url, data={}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(self.banner_url, data={}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_employee(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.put(self.banner_url, data={}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(self.banner_url, data={}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_moderator(self):
        employee, emp_user = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_user)
        data = banner_fake_data(json=True, title='xxx', order=1)
        res = self.client.put(self.banner_url, data=data, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        banner = BannerAdd.objects.get(pk=self.banner.pk)
        self.assertEqual(banner.title, 'xxx')

        data = {
            'title': 'yyy',
        }
        res = self.client.patch(self.banner_url, data=data, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        banner = BannerAdd.objects.get(pk=self.banner.pk)
        self.assertEqual(banner.title, 'yyy')


class BannerAddViewDeleteTest(APITestCase):

    def setUp(self) -> None:

        Group.objects.create(name='moderator')
        self.banner = create_banner()
        self.banner_url = reverse('banners-detail', args=[self.banner.pk,])

    def test_no_auth(self):
        res = self.client.delete(self.banner_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.delete(self.banner_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_employee(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.delete(self.banner_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_employee_moderator(self):
        employee, emp_moderator = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_moderator)
        res = self.client.delete(self.banner_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

class BannerAddViewQuerySetTest(APITestCase):

    def setUp(self) -> None:
        self.banners_url = reverse('banners-list')
        for _ in range(3):
            create_banner()

        add = BannerAdd.objects.last()
        add.is_public = False
        add.save()

    def test_no_auth(self):
        res = self.client.get(self.banners_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.banners_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_employee(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.get(self.banners_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_employee_moderator(self):
        employee, emp_user = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_user)
        res = self.client.get(self.banners_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

