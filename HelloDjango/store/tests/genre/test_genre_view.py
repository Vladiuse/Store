from rest_framework.test import APITestCase
from store.models import Book, Genre, Author, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.reverse import reverse
from rest_framework import status
from _helptools import str_random, create_book, create_employee_user, create_genre, create_author, create_user


class GenreViewRetrieveTest(APITestCase):

    def setUp(self) -> None:
        self.genre = create_genre()
        self.genre_list_url = reverse('genre-list')
        self.genre_detail_url = reverse('genre-detail', args=[self.genre.pk,])

    def test_no_auth(self):
        res = self.client.get(self.genre_detail_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.genre_detail_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_employee_auth(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.get(self.genre_detail_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_moderator_auth(self):
        employee, emp_user = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_user)
        res = self.client.get(self.genre_detail_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

class GenreViewListTest(APITestCase):

    def setUp(self) -> None:
        self.genre_list_url = reverse('genre-list')

    def test_no_auth(self):
        res = self.client.get(self.genre_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.genre_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_employee_auth(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.get(self.genre_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_moderator_auth(self):
        employee, emp_user = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_user)
        res = self.client.get(self.genre_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

class GenreViewCreateTest(APITestCase):

    def setUp(self) -> None:
        self.genre_list_url = reverse('genre-list')

        Group.objects.create(name='moderator')

    def test_no_auth(self):
        res = self.client.post(self.genre_list_url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.post(self.genre_list_url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_auth(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.post(self.genre_list_url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_auth(self):
        employee, emp_user = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_user)
        data={
            'name': 'test',
        }
        res = self.client.post(self.genre_list_url, data=data,format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 1)


class GenreUpdateViewTest(APITestCase):

    def setUp(self) -> None:
        self.genre = create_genre()
        self.genre_detail_url = reverse('genre-detail', args=[self.genre.pk,])

        Group.objects.create(name='moderator')


    def test_no_auth(self):
        res = self.client.put(self.genre_detail_url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(self.genre_detail_url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.put(self.genre_detail_url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(self.genre_detail_url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_auth(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.put(self.genre_detail_url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.patch(self.genre_detail_url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_auth(self):
        employee, emp_user = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_user)
        data={
            'name': 'test',
        }
        res = self.client.put(self.genre_detail_url, data=data,format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Genre.objects.count(), 1)

        res = self.client.patch(self.genre_detail_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Genre.objects.count(), 1)


class GenreViewDeleteTest(APITestCase):
    def setUp(self) -> None:
        self.genre = create_genre()
        self.genre_detail_url = reverse('genre-detail', args=[self.genre.pk,])

        Group.objects.create(name='moderator')

    def test_no_auth(self):
        res = self.client.delete(self.genre_detail_url,format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.delete(self.genre_detail_url,format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_auth(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.delete(self.genre_detail_url,format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_auth(self):
        employee, emp_user = create_employee_user(add_group='moderator')
        self.client.force_login(user=emp_user)
        res = self.client.delete(self.genre_detail_url,format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)



