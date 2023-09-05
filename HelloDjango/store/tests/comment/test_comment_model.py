from django.test import TestCase
from store.models import Comment, Book
from _helptools import create_book, create_user


class CommentModelStarStatTest(TestCase):

    def test_starts_stat_no_comments(self):
        qs = Comment.objects.all()
        expected = {star:0 for star in range(1, Comment.STAR_MAX_VALUE + 1)}
        stat = Comment.stars_stat(qs)
        self.assertEqual(stat, expected)

    def test_star_stat_all_five(self):
        book = create_book()
        for _ in range(3):
            Comment.objects.create(
                book=book,
                owner=create_user(),
                text='123',
                stars=Comment.STAR_MAX_VALUE
            )
        expected = {star:0 for star in range(1, Comment.STAR_MAX_VALUE + 1)}
        expected[5] = 3
        qs = Comment.objects.all()
        stat = Comment.stars_stat(qs)
        self.assertEqual(stat, expected)

    def test_star_stat_querys_count(self):
        book = create_book()
        for _ in range(3):
            Comment.objects.create(
                book=book,
                owner=create_user(),
                text='123',
                stars=Comment.STAR_MAX_VALUE
            )
        expected = {star:0 for star in range(1, Comment.STAR_MAX_VALUE + 1)}
        expected[5] = 3
        qs = Comment.objects.all()
        stat = Comment.stars_stat(qs)
        self.assertEqual(stat, expected)
        self.assertNumQueries(1)

    def test_two_books_w_comms(self):
        book_1 = create_book()
        book_2 = create_book()
        comms = []
        for book in (book_1, book_2):
            for _ in range(3):
                comm = Comment(
                    book=book,
                    owner=create_user(),
                    text='123',
                    stars=Comment.STAR_MAX_VALUE
                )
                comms.append(comm)
        Comment.objects.bulk_create(comms)

        qs = Comment.objects.filter(book=book_1)
        self.assertEqual(len(qs), 3)
        expected = {star: 0 for star in range(1, Comment.STAR_MAX_VALUE + 1)}
        expected[5] = 3
        stat = Comment.stars_stat(qs)
        self.assertEqual(stat, expected)
        expected[5] = 3

    def test_type_passed_attrs(self):
        book = create_book()
        comms = []
        for _ in range(3):
            c = Comment(
                book=book,
                owner=create_user(),
                text='123',
                stars=Comment.STAR_MAX_VALUE
            )
            comms.append(c)
        Comment.objects.bulk_create(comms)
        qs = list()
        self.assertRaises(TypeError, Comment.stars_stat, qs)

    def test_not_book_qs(self):
        book = create_book()
        comms = []
        for _ in range(3):
            c = Comment(
                book=book,
                owner=create_user(),
                text='123',
                stars=Comment.STAR_MAX_VALUE
            )
            comms.append(c)
        Comment.objects.bulk_create(comms)
        qs = Book.objects.all()
        self.assertRaises(TypeError, Comment.stars_stat, qs)
