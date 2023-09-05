from django.test import TestCase
from store.models import Comment, Book, Like
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


class CommentLikeTest(TestCase):

    def setUp(self) -> None:
        self.book = create_book()
        self.user = create_user()

    def test_add_like_no_like(self):
        comment = Comment.objects.create(
            book=self.book,
            owner=self.user,
            text='123',
            stars=5,
        )
        self.assertEqual(Like.objects.count(),0)
        like = comment.set_like(self.user)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(like.flag, 1)
        self.assertNumQueries(4)

    def test_set_like_no_created(self):
        comment = Comment.objects.create(
            book=self.book,
            owner=self.user,
            text='123',
            stars=5,
        )
        Like.objects.create(comment=comment, owner=self.user, flag=True)
        self.assertEqual(Like.objects.count(),1)
        like = comment.set_like(self.user)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(like.flag, 1)
        self.assertNumQueries(5)


    def test_set_dislike_no_like(self):
        comment = Comment.objects.create(
            book=self.book,
            owner=self.user,
            text='123',
            stars=5,
        )
        self.assertEqual(Like.objects.count(),0)
        like = comment.set_dislike(self.user)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(like.flag, 0)
        self.assertNumQueries(4)

    def test_set_dislike_like_created(self):
        comment = Comment.objects.create(
            book=self.book,
            owner=self.user,
            text='123',
            stars=5,
        )
        Like.objects.create(comment=comment, owner=self.user, flag=False)
        self.assertEqual(Like.objects.count(), 1)
        like = comment.set_dislike(self.user)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(like.flag, 0)
        self.assertNumQueries(5)

    def test_change_like_flag_to_like(self):
        comment = Comment.objects.create(
            book=self.book,
            owner=self.user,
            text='123',
            stars=5,
        )
        comment.set_like(self.user)
        self.assertEqual(Like.objects.count(),1)
        like = Like.objects.get(owner=self.user, comment=comment)
        self.assertEqual(like.flag, 1)
        comment.set_dislike(self.user)
        self.assertEqual(Like.objects.count(), 1)
        like = Like.objects.get(owner=self.user, comment=comment)
        self.assertEqual(like.flag, 0)

    def test_change_like_flag_on_like(self):
        comment = Comment.objects.create(
            book=self.book,
            owner=self.user,
            text='123',
            stars=5,
        )
        comment.set_dislike(self.user)
        self.assertEqual(Like.objects.count(), 1)
        like = Like.objects.get(owner=self.user, comment=comment)
        self.assertEqual(like.flag, 0)
        comment.set_like(self.user)
        self.assertEqual(Like.objects.count(), 1)
        like = Like.objects.get(owner=self.user, comment=comment)
        self.assertEqual(like.flag, 1)

    def test_set_like_user_model_attr(self):
        comment = Comment.objects.create(
            book=self.book,
            owner=self.user,
            text='123',
            stars=5,
        )
        self.assertRaises(TypeError, comment.set_like, list())
        self.assertRaises(TypeError, comment.set_dislike, list())

class CommentUserLikeTest(TestCase):

    def setUp(self) -> None:
        self.book = create_book()
        self.user = create_user()
        self.comment = Comment.objects.create(owner=self.user, book=self.book, stars=1)
        self.users = [create_user() for _ in range(3)]

        for user in self.users:
            self.comment.set_like(user)

    def test_no_user_like(self):
        self.assertEqual(self.comment.user_like(self.user),None)
        self.assertNumQueries(1)

    def test_user_like(self):
        self.comment.set_like(self.user)
        like = self.comment.user_like(self.user)
        self.assertTrue(isinstance(like, Like))

    def test_user_like_no_likes_on_comment(self):
        user = create_user()
        comment = Comment.objects.create(owner=user, book=self.book, stars=1)
        self.assertEqual(comment.user_like(user), None)







