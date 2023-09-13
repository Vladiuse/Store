from store.models import Basket, Book
from store.errors import LatsBasketItemError
from django.test import TestCase
from _helptools import create_book, create_user
from django.db import IntegrityError


class BasketDefaultValueTest(TestCase):


    def test_one(self):
        self.book = create_book(price=200)
        self.user = create_user()
        basket = Basket.objects.create(book=self.book, owner=self.user)
        self.assertEqual(basket.quantity, 1)

class BasketModelQuerySetTest(TestCase):
    def setUp(self) -> None:
        self.book_1 = create_book(price=100)
        self.book_2 = create_book(price=200)
        self.user = create_user()

    def test_sum_no_elems(self):
        qs = Basket.objects.filter(owner=self.user)
        self.assertEqual(qs.total_sum(), 0)

    def test_total_sum(self):
        basket_1 = Basket.objects.create(book=self.book_1, owner=self.user)
        basket_2 = Basket.objects.create(book=self.book_2, owner=self.user)
        qs = Basket.objects.filter(owner=self.user)
        self.assertEqual(qs.total_sum(), 100 + 200)

    def test_total_sum_few_quantity(self):
        basket_1 = Basket.objects.create(book=self.book_1, owner=self.user, quantity=5)
        basket_2 = Basket.objects.create(book=self.book_2, owner=self.user, quantity=10)
        qs = Basket.objects.filter(owner=self.user)
        self.assertEqual(qs.total_sum(), 100*5 + 200*10)

    def test_total_quantity_no_elems(self):
        qs = Basket.objects.filter(owner=self.user)
        self.assertEqual(qs.total_quantity(), 0)

    def test_total_quantity_few(self):
        basket_1 = Basket.objects.create(book=self.book_1, owner=self.user, quantity=5)
        basket_2 = Basket.objects.create(book=self.book_2, owner=self.user, quantity=10)
        qs = Basket.objects.filter(owner=self.user)
        self.assertEqual(qs.total_quantity(), 15)


class BasketModelSumMethodTest(TestCase):

    def setUp(self) -> None:
        self.book_1 = create_book(price=100)
        self.book_2 = create_book(price=200)
        self.user = create_user()

    def test_one_item(self):
        basket = Basket.objects.create(book=self.book_1, owner=self.user)
        self.assertEqual(basket.sum, 100)

    def test_few_item(self):
        basket = Basket.objects.create(book=self.book_1, owner=self.user, quantity=5)
        self.assertEqual(basket.sum, 500)


class BasketModelAddMethodTest(TestCase):
    def setUp(self) -> None:
        self.book_1 = create_book(price=100)
        self.book_2 = create_book(price=200)
        self.book_3 = create_book(price=300)
        self.user = create_user()

    def test_add_no_item(self):
        Basket.add(self.book_1,self.user)
        self.assertTrue(Basket.objects.filter(book=self.book_1, owner=self.user).exists())
        basket_qs = Basket.objects.filter(owner=self.user)
        self.assertEqual(basket_qs.total_quantity(), 1)

    def test_add_no_item_quantity_val(self):
        Basket.add(self.book_1,self.user)
        basket = Basket.objects.get(book=self.book_1, owner=self.user)
        self.assertEqual(basket.quantity, 1)

    def test_add_item_basket_exist(self):
        basket = Basket.objects.create(owner=self.user, book=self.book_1)
        self.assertRaises(IntegrityError, Basket.add, self.book_1, self.user)

    def test_add_few_books(self):
        Basket.add(self.book_1, self.user)
        Basket.add(self.book_2, self.user)
        Basket.add(self.book_3, self.user)
        basket_qs = Basket.objects.filter(owner=self.user)
        self.assertEqual(basket_qs.total_quantity(), 3)



# class BasketModelRemoveMethodTest(TestCase):  # TODO delete
#     def setUp(self) -> None:
#         self.book_1 = create_book(price=100)
#         self.book_2 = create_book(price=200)
#         self.book_3 = create_book(price=300)
#         self.user = create_user()
#
#     def test_remove_no_items(self):
#         self.assertRaises(Basket.DoesNotExist, Basket.remove,self.book_1, self.user)
#
#     def test_remove_one_item_exist(self):
#         Basket.objects.create(owner=self.user, book=self.book_1)
#         self.assertEqual(Basket.objects.count(),1)
#         self.assertRaises(LatsBasketItemError, Basket.remove,self.book_1, self.user)
#
#     def test_remove_few_items_exists(self):
#         Basket.objects.create(owner=self.user, book=self.book_1, quantity=3)
#         self.assertEqual(Basket.objects.count(),1)
#         basket = Basket.remove(self.book_1, self.user)
#         self.assertEqual(basket.quantity,2)
#
#     def test_remove_few_items_exists_2(self):
#         Basket.objects.create(owner=self.user, book=self.book_1, quantity=3)
#         Basket.objects.create(owner=self.user, book=self.book_2, quantity=3)
#         Basket.objects.create(owner=self.user, book=self.book_3, quantity=3)
#         self.assertEqual(Basket.objects.count(), 3)
#         basket = Basket.remove(self.book_1, self.user)
#         self.assertEqual(basket.quantity, 2)
#         self.assertEqual(Basket.objects.count(), 3)












