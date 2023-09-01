from django.test import TestCase
from os import path
from faker import Faker
from store.models import Book, Genre, Author
import random as r
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import QuerySet

f = Faker()
from _helpers import str_random



def create_genre():
    return Genre.objects.create(name=str_random())


def create_author():
    return Author.objects.create(name=str_random())


def create_book(genre=None):
    test_image_path = './HelloDjango/store/tests/book/book_cover.webp'
    book = Book.objects.create(
        name=str_random(),
        # genre=(create_genre(),),
        price=round(r.random() * 100, 2),
        author=create_author(),
        available_in_store=r.randint(1, 5),
        description=f.paragraph(nb_sentences=5),
        img_cover=SimpleUploadedFile(
            name='x.jpg',
            content=open(test_image_path, 'rb').read(),
            content_type=f'image/jpg'),
    )
    if not genre:
        genre = create_genre()
    book.genre.add(genre)
    return book


class BookModelTest(TestCase):

    def test_manager_all(self):
        for _ in range(3):
            create_book()
        self.assertEqual(Book.objects.count(), 3)

    def test_manager_public(self):
        for _ in range(3):
            book = create_book()
            book.is_public = False
            book.save()
        self.assertEqual(Book.public.count(), 0)

    def test_similar_book_only_on_genre_correct_count(self):
        genre = create_genre()
        for _ in range(10):
            create_book(genre=genre)
        book = Book.public.last()
        similar_books = book.similar_books()
        self.assertEqual(len(similar_books), Book.SIMILAR_BOOKS_COUNT)

    def test_similar_books_return_qs(self):
        genre = create_genre()
        for _ in range(10):
            create_book(genre=genre)
        book = Book.public.last()
        similar_books = book.similar_books()
        self.assertTrue(isinstance(similar_books, QuerySet))

    def test_similar_books_different_genres(self):
        genre_1 = create_genre()
        genre_2 = create_genre()
        book = create_book(genre=genre_1)
        for _ in range(10):
            create_book(genre_2)
        similar_books = book.similar_books()
        self.assertEqual(len(similar_books), Book.SIMILAR_BOOKS_COUNT)

    def test_similar_book_one_book_in_db(self):
        book = create_book()
        similar_book = book.similar_books()
        self.assertEqual(len(similar_book), 0)


    def test_delete_img_with_book(self):
        book = create_book()
        img_cover_path = book.img_cover.path
        self.assertTrue(path.exists(img_cover_path))
        book.delete()
        self.assertFalse(path.exists(img_cover_path))
