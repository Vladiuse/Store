from rest_framework.test import APITestCase
import json
from rest_framework.reverse import reverse
from store.models import Comment, Book, Like
from _helptools import create_user, create_employee_user, create_book
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class BookCommentListTest(APITestCase):

    def setUp(self) -> None:
        self.book = create_book()
        self.user = create_user()
        self.users = []
        self.book_coms_url = reverse('book-comment-list', args=[self.book.pk, ])

        for _ in range(5):
            user = User(username='name' + str(_), password='0000')
            self.users.append(user)
        User.objects.bulk_create(self.users)

        coms = list()
        for user in self.users:
            comm = Comment(owner=user, book=self.book, text='123', stars=1)
            coms.append(comm)
        Comment.objects.bulk_create(coms)

    def test_list_no_auth(self):
        res = self.client.get(self.book_coms_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['comments']), 5)

    def test_list_auth_user(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.book_coms_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['comments']), 5)

    def test_list_no_own_comment(self):
        self.client.force_login(user=self.user)
        res = self.client.get(self.book_coms_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['comments']), 5)
        self.assertIsNone(res.data['user_comment'])

    def test_list_own_comment(self):
        Comment.objects.create(book=self.book, owner=self.user, text='123', stars=1)
        self.client.force_login(user=self.user)
        res = self.client.get(self.book_coms_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['comments']), 5)
        user_comment = res.data['user_comment']
        self.assertEqual(user_comment['text'], '123')
        self.assertEqual(user_comment['owner'], self.user.pk)

    def test_no_comments(self):
        Comment.objects.all().delete()
        self.assertEqual(Comment.objects.count(), 0)
        res = self.client.get(self.book_coms_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['comments']), 0)


class BookCommentCreateViewTest(APITestCase):
    def setUp(self) -> None:
        self.book = create_book()
        self.user = create_user()
        self.users = []
        self.book_coms_url = reverse('book-comment-list', args=[self.book.pk, ])

        for _ in range(5):
            user = User(username='name' + str(_), password='0000')
            self.users.append(user)
        User.objects.bulk_create(self.users)

        coms = list()
        for user in self.users:
            comm = Comment(owner=user, book=self.book, text='123', stars=1)
            coms.append(comm)
        Comment.objects.bulk_create(coms)

    def test_no_auth(self):
        res = self.client.post(self.book_coms_url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user(self):
        self.client.force_login(user=self.user)
        comment_data = {
            'text': '123',
            'stars': 1,
        }
        res = self.client.post(self.book_coms_url, data=comment_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_auth_user_second_comment(self):
        self.client.force_login(user=self.user)
        comment_data = {
            'text': '123',
            'stars': 1,
        }
        res = self.client.post(self.book_coms_url, data=comment_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post(self.book_coms_url, data=comment_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class CommentViewRetrieveTest(APITestCase):

    def setUp(self) -> None:
        self.book = create_book()
        self.user = create_user()
        self.comment = Comment.objects.create(
            book=self.book, owner=self.user, stars=1, text='123'
        )
        self.comm_url = reverse('comment-detail',args=[self.comment.pk,])

    def test_get_comment_no_auth(self):
        res = self.client.get(self.comm_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_user(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.comm_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_no_exist_comment(self):
        url = reverse('comment-detail', args=[1001,])
        self.client.force_login(user=self.user)
        res = self.client.get(url,format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class CommentViewUpdateTest(APITestCase):
    def setUp(self) -> None:
        self.book = create_book()
        self.user = create_user()
        self.comment = Comment.objects.create(
            book=self.book, owner=self.user, stars=1, text='123'
        )
        self.comm_url = reverse('comment-detail',args=[self.comment.pk,])

    def test_update_no_auth(self):
        res = self.client.put(self.comm_url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.patch(self.comm_url,data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_onw_comment(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.put(self.comm_url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.patch(self.comm_url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_own_comment(self):
        self.client.force_login(user=self.user)
        data = {
            'text': 'xxx',
            'stars': 1,
        }
        res = self.client.put(self.comm_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        comment = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(comment.text, 'xxx')
        data = {
            'text': 'yyy',
        }
        res = self.client.patch(self.comm_url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        comment = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(comment.text, 'yyy')

    def test_no_exist_comment(self):
        url = reverse('comment-detail', args=[1001,])
        self.client.force_login(user=self.user)
        res = self.client.put(url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        res = self.client.patch(url, data={},format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class CommentViewDeleteTest(APITestCase):
    def setUp(self) -> None:
        self.book = create_book()
        self.user = create_user()
        self.comment = Comment.objects.create(
            book=self.book, owner=self.user, stars=1, text='123'
        )
        self.comm_url = reverse('comment-detail',args=[self.comment.pk,])

    def test_no_auth_user(self):
        res = self.client.delete(self.comm_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_own_comment(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.delete(self.comm_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_own_comment(self):
        self.client.force_login(user=self.user)
        res = self.client.delete(self.comm_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_no_exist_comment(self):
        url = reverse('comment-detail', args=[1001,])
        self.client.force_login(user=self.user)
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class CommentDetailViewSetLikeTest(APITestCase):

    def setUp(self) -> None:
        self.book = create_book()
        self.user = create_user()
        self.comment = Comment.objects.create(
            owner=self.user,
            book=self.book,
            text='123',
            stars=1,
        )
        self.like_url = reverse('comment-like', args=[self.comment.pk, ])
        self.dislike_url = reverse('comment-dislike', args=[self.comment.pk, ])

    def test_no_auth_like(self):
        res = self.client.post(self.like_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_auth_dislike(self):
        res = self.client.post(self.dislike_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_like(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.post(self.like_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_auth_user_dislike(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.post(self.dislike_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_remove_like_no_auth(self):
        Like.objects.create(comment=self.comment, owner=self.user, flag=True)
        self.assertEqual(Like.objects.count(),1)
        res = self.client.delete(self.like_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_like_auth(self):
        self.client.force_login(user=self.user)
        Like.objects.create(comment=self.comment, owner=self.user, flag=True)
        self.assertEqual(Like.objects.count(),1)
        res = self.client.delete(self.like_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(),0)

    def test_remove_like_autt_no_like_created(self):
        # Like.objects.create(comment=self.comment, owner=self.user, flag=True)
        self.client.force_login(user=self.user)
        self.assertEqual(Like.objects.count(),0)
        res = self.client.delete(self.like_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_dislike_no_auth(self):
        Like.objects.create(comment=self.comment, owner=self.user, flag=False)
        self.assertEqual(Like.objects.count(),1)
        res = self.client.delete(self.dislike_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_dislike_auth(self):
        self.client.force_login(user=self.user)
        Like.objects.create(comment=self.comment, owner=self.user, flag=False)
        self.assertEqual(Like.objects.count(),1)
        res = self.client.delete(self.dislike_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(),0)

    def test_remove_like_autt_no_dislike_created(self):
        # Like.objects.create(comment=self.comment, owner=self.user, flag=True)
        self.client.force_login(user=self.user)
        self.assertEqual(Like.objects.count(),0)
        res = self.client.delete(self.dislike_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

class CommentUserLikeSerializerTest(APITestCase):

    def setUp(self) -> None:
        self.book = create_book()
        self.user = create_user()
        self.comment = Comment.objects.create(
            owner=self.user,
            book=self.book,
            text='123',
            stars=1,
        )
        self.comment_url = reverse('comment-detail', args=[self.comment.pk,])
        self.book_coms_url = reverse('book-comment-list', args=[self.book.pk, ])

    def test_no_auth(self):
        res = self.client.get(self.book_coms_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content)
        comment = data['comments'][0]
        self.assertEqual(comment['user_like'], None)

    def test_auth_no_user_like(self):
        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.book_coms_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content)
        comment = data['comments'][0]
        self.assertEqual(comment['user_like'], None)

    def test_user_like_exist(self):
        user = create_user()
        self.client.force_login(user=user)
        self.comment.set_like(user)
        res = self.client.get(self.book_coms_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content)
        comment = data['comments'][0]
        user_like = Like.objects.get(comment=self.comment, owner=user)
        self.assertIsNotNone(comment['user_like'])
        self.assertEqual(comment['user_like']['id'], user_like.pk)





