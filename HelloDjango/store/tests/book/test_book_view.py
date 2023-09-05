from rest_framework.test import APITestCase
from os import path
from faker import Faker
from store.models import Book, Genre, Author, Comment
import random as r
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .test_book_model import create_book
from rest_framework.reverse import reverse
from rest_framework import status
from _helptools import create_employee_user, create_user, get_book_fake_data, create_genre

User = get_user_model()


class BookViewListTest(APITestCase):

    # NO AUTH
    def test_no_auth(self):
        url = reverse('book-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_no_auth_content_len(self):
        for _ in range(3):
            book = create_book()
        url = reverse('book-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_no_auth_len_content_2(self):
        create_book()
        for _ in range(3):
            create_book(is_public=False)
        url = reverse('book-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    # AUTH
    def test_auth(self):
        user = User.objects.create(username='xxx', password='xxx')
        self.client.force_login(user=user)
        url = reverse('book-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_content_len(self):
        user = User.objects.create(username='xxx', password='xxx')
        self.client.force_login(user=user)
        for _ in range(3):
            book = create_book()
        url = reverse('book-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_auth_len_content_2(self):
        user = User.objects.create(username='xxx', password='xxx')
        self.client.force_login(user=user)
        create_book()
        for _ in range(3):
            create_book(is_public=False)
        url = reverse('book-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    # EMPLOYEE

    def test_employee_no_content(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        url = reverse('book-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_employee_content(self):
        create_book()
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        url = reverse('book-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)


class BookViewGetTest(APITestCase):

    def test_no_auth(self):
        book = create_book()
        url = reverse('book-detail', args=[book.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_user(self):
        user = create_user()
        self.client.force_login(user=user)
        book = create_book()
        url = reverse('book-detail', args=[book.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_employee(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        book = create_book()
        url = reverse('book-detail', args=[book.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrive_not_public_book_no_auth(self):
        book = create_book(is_public=False)
        url = reverse('book-detail', args=[book.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrive_not_public_auth(self):
        user = create_user()
        self.client.force_login(user=user)
        book = create_book(is_public=False)
        url = reverse('book-detail', args=[book.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrive_not_public_employee(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        book = create_book(is_public=False)
        url = reverse('book-detail', args=[book.pk, ])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class BookViewCreateTest(APITestCase):

    def test_no_auth(self):
        url = reverse('book-list')
        res = self.client.post(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user(self):
        user = create_user()
        self.client.force_login(user=user)
        url = reverse('book-list')
        res = self.client.post(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_not_moderator(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        url = reverse('book-list')
        res = self.client.post(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_moderator_user(self):
        employee, emp_user = create_employee_user()
        moderators_group = Group.objects.create(name='moderator')
        emp_user.groups.add(moderators_group)
        self.client.force_login(user=emp_user)
        url = reverse('book-list')
        data=get_book_fake_data(json=True)
        genre = create_genre()
        data['genre'] = genre.pk
        res = self.client.post(url, data=data, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)




class BookViewUpdateTest(APITestCase):

    def setUp(self) -> None:
        self.book = create_book()

    def test_no_auth_user(self):
        url = reverse('book-detail', args=[self.book.pk,])
        res = self.client.put(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.patch(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user(self):
        user = create_user()
        self.client.force_login(user=user)
        url = reverse('book-detail', args=[self.book.pk, ])
        res = self.client.put(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.patch(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_employee(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        url = reverse('book-detail', args=[self.book.pk, ])
        res = self.client.put(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.patch(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_moderator_put(self):
        employee, moderator_user = create_employee_user(add_group='moderator')
        self.client.force_login(moderator_user)
        url = reverse('book-detail', args=[self.book.pk, ])
        data=get_book_fake_data(json=True)
        genre = create_genre()
        data['genre'] = genre.pk
        res = self.client.put(url, data=data, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_moderator_patch(self):
        employee, moderator_user = create_employee_user(add_group='moderator')
        self.client.force_login(moderator_user)
        url = reverse('book-detail', args=[self.book.pk, ])
        data = {'name': '123'}
        res = self.client.patch(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class BookViewDeleteTest(APITestCase):

    def setUp(self) -> None:
        self.book = create_book()
        self.book_url = reverse('book-detail', args=[self.book.pk,])


    def test_no_auth_user(self):
        res = self.client.delete(self.book_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.delete(self.book_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_employee(self):
        employee, emp_user = create_employee_user()
        self.client.force_login(user=emp_user)
        res = self.client.delete(self.book_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator(self):
        employee, moderator_user = create_employee_user(add_group='moderator')
        self.client.force_login(user=moderator_user)
        res = self.client.delete(self.book_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)



