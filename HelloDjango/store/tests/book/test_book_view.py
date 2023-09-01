from rest_framework.test import APITestCase
from os import path
from faker import Faker
from store.models import Book, Genre, Author, Comment
import random as r
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from .test_book_model import create_book
from rest_framework.reverse import reverse
from rest_framework import status
from .test_book_model import create_book
from _helptools import create_employee_user, create_user

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

    pass
    # TODO


class BookViewUpdateTest(APITestCase):
    pass
    # TODO


class BookViewDeleteTest(APITestCase):
    pass
    # TODO
