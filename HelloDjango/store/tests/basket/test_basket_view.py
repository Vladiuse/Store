from rest_framework.test import APITestCase
from store.models import Basket
from _helptools import create_book, create_user
from rest_framework.reverse import reverse
from rest_framework import status


class BasketViewListTest(APITestCase):
    def setUp(self) -> None:
        self.book_1 = create_book(price=100)
        self.book_2 = create_book(price=200)
        self.book_3 = create_book(price=300)
        self.user = create_user()
        self.add_book_1 = reverse('book-add-to-basket', args=[self.book_1.pk,])
        self.add_book_2 = reverse('book-add-to-basket', args=[self.book_2.pk,])
        self.add_book_3 = reverse('book-add-to-basket', args=[self.book_3.pk,])
        self.basket_list_url = reverse('basket-list')

    def test_no_auth(self):
        res = self.client.get(self.basket_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_empty(self):
        self.client.force_login(user=self.user)
        res = self.client.get(self.basket_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),0)

    def test_one_item(self):
        self.client.force_login(user=self.user)
        self.client.post(self.add_book_1)
        res = self.client.get(self.basket_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_few_item(self):
        self.client.force_login(user=self.user)
        for url in (self.add_book_1,self.add_book_2,self.add_book_3):
            self.client.post(url, format='json')
        res = self.client.get(self.basket_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_not_see_other(self):
        self.client.force_login(user=self.user)
        self.client.post(self.add_book_1)
        res = self.client.get(self.basket_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

        user = create_user()
        self.client.force_login(user=user)
        res = self.client.get(self.basket_list_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

class BasketViewUpdateTest(APITestCase):
    def setUp(self) -> None:
        self.book_1 = create_book(price=100)
        self.book_2 = create_book(price=200)
        self.book_3 = create_book(price=300)
        self.user = create_user()
        self.add_book_1 = reverse('book-add-to-basket', args=[self.book_1.pk,])
        self.add_book_2 = reverse('book-add-to-basket', args=[self.book_2.pk,])
        self.add_book_3 = reverse('book-add-to-basket', args=[self.book_3.pk,])
        self.basket_list_url = reverse('basket-list')

    def test_up_quantity_no_auth(self):
        basker = Basket.add(self.book_1, self.user)
        url = reverse('basket-detail', args=[basker.pk,])
        data = {}
        res = self.client.patch(url, data=data,format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_up_quantity_auth_onw(self):
        self.client.force_login(user=self.user)
        basket = Basket.add(self.book_1, self.user)
        url = reverse('basket-detail', args=[basket.pk,])
        data = {
            'quantity':3,
        }
        res = self.client.patch(url, data=data,format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        basket.refresh_from_db()
        self.assertEqual(basket.quantity, 3)

    def test_drop_down_quantity(self):
        self.client.force_login(user=self.user)
        basket = Basket.objects.create(book=self.book_1, owner=self.user, quantity=3)
        url = reverse('basket-detail', args=[basket.pk,])
        data = {
            'quantity':1,
        }
        res = self.client.patch(url, data=data,format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        basket.refresh_from_db()
        self.assertEqual(basket.quantity, 1)

    def test_change_quantity_not_own(self):
        self.client.force_login(user=self.user)
        user = create_user()
        basket = Basket.objects.create(book=self.book_1, owner=user, quantity=3)
        url = reverse('basket-detail', args=[basket.pk, ])
        data = {
            'quantity': 1,
        }
        res = self.client.patch(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


    def test_drop_down_quantity_lt_one(self):
        self.client.force_login(user=self.user)
        basket = Basket.objects.create(book=self.book_1, owner=self.user, quantity=3)
        url = reverse('basket-detail', args=[basket.pk,])
        data = {
            'quantity':0,
        }
        res = self.client.patch(url, data=data,format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, msg=res.data)
        basket.refresh_from_db()
        self.assertEqual(basket.quantity, 3)


    def test_drop_down_quantity_gt_max_val(self):
        self.client.force_login(user=self.user)
        basket = Basket.objects.create(book=self.book_1, owner=self.user, quantity=3)
        url = reverse('basket-detail', args=[basket.pk,])
        data = {
            'quantity':Basket.MAX_QUANTITY + 3,
        }
        res = self.client.patch(url, data=data,format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, msg=res.data)
        basket.refresh_from_db()
        self.assertEqual(basket.quantity, 3)


class BasketViewDeleteTest(APITestCase):

    def setUp(self) -> None:
        self.book_1 = create_book(price=100)
        self.book_2 = create_book(price=200)
        self.book_3 = create_book(price=300)
        self.user = create_user()
        self.add_book_1 = reverse('book-add-to-basket', args=[self.book_1.pk,])
        self.add_book_2 = reverse('book-add-to-basket', args=[self.book_2.pk,])
        self.add_book_3 = reverse('book-add-to-basket', args=[self.book_3.pk,])
        self.basket_list_url = reverse('basket-list')

    def test_no_auth(self):
        basket = Basket.add(self.book_1, self.user)
        url = reverse('basket-detail', args=[basket.pk,])
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Basket.objects.count(),1)


    def test_auth_own(self):
        basket = Basket.add(self.book_1, self.user)
        url = reverse('basket-detail', args=[basket.pk,])
        self.client.force_login(user=self.user)
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Basket.objects.count(),0)

    def test_auth_not_own(self):
        user = create_user()
        basket = Basket.add(self.book_1, user)
        url = reverse('basket-detail', args=[basket.pk,])
        self.client.force_login(user=self.user)
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Basket.objects.count(),1)

    def test_auth_own_few_items(self):
        self.client.force_login(user=self.user)
        for url in (self.add_book_1,self.add_book_2,self.add_book_3):
            self.client.post(url, format='json')
        self.assertEqual(Basket.objects.filter(owner=self.user).count(),3)
        basket = Basket.objects.get(owner=self.user, book=self.book_1)
        url = reverse('basket-detail', args=[basket.pk,])
        res = self.client.delete(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Basket.objects.filter(owner=self.user).count(),2)
        self.assertFalse(Basket.objects.filter(owner=self.user, book=self.book_1).exists())






