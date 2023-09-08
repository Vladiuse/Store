from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from store.models import Book, Comment, Favorite
from django.contrib.auth import get_user_model
from _helptools import create_user, create_book
import json

User = get_user_model()


class FavoriteBookViewTest(APITestCase):

    def setUp(self) -> None:
        self.user_1 = create_user()
        self.user_2 = create_user()
        self.favorite_url = reverse('favorite-books')

        self.create_books_n_favs()

    def create_books_n_favs(self):
        for _ in range(10):
            create_book()

        qs_1 = Book.objects.filter(pk__in=[1, 2, 3])
        qs_2 = Book.objects.filter(pk__in=[4, 5,])
        [Favorite.objects.create(book=book, owner=self.user_1) for book in qs_1]
        [Favorite.objects.create(book=book, owner=self.user_2) for book in qs_2]

    def test_no_auth_user(self):
        res = self.client.get(self.favorite_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_1(self):
        self.client.force_login(user=self.user_1)
        res = self.client.get(self.favorite_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_user_2(self):
        self.client.force_login(user=self.user_2)
        res = self.client.get(self.favorite_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_user_1_correct_books(self):
        self.client.force_login(user=self.user_1)
        res = self.client.get(self.favorite_url, format='json')
        data = json.loads(res.content)
        result_books_ids = {book['id'] for book in data}
        self.assertEqual(result_books_ids, {1,2,3})

    def test_user_2_correct_books(self):
        self.client.force_login(user=self.user_2)
        res = self.client.get(self.favorite_url, format='json')
        data = json.loads(res.content)
        result_books_ids = {book['id'] for book in data}
        self.assertEqual(result_books_ids, {4,5})

    def test_no_favs(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.favorite_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),0)
