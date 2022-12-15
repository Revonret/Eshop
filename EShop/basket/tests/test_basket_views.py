from user.models import UserBase
from django.test import TestCase
from django.urls import reverse

from shopping.models import Category, Product


class HomepageTests(TestCase):
    def test_summary(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)


class TestBasketView(TestCase):
    def setUp(self):
        UserBase.objects.create(user_name='admin')
        a = Category.objects.create(name='django', slug='django')
        Product.objects.create(category=a, product_name='django beginners', in_stock=5,
                               slug='django-beginners', price='20.00', description='testtesttest')
        Product.objects.create(category=a, product_name='django intermediate', in_stock=3,
                               slug='django-intermediate', price='20.00', description='testtesttest')
        Product.objects.create(category=a, product_name='django advanced', in_stock=2,
                               slug='django-advanced', price='20.00', description='testtesttesttest')
        self.client.post(
            reverse('basket:basket_add'), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(
            reverse('basket:basket_add'), {"productid": 2, "productqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": 3, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_delete(self):
        response = self.client.post(
            reverse('basket:basket_delete'), {"productid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '20.00'})

    def test_basket_update(self):

        response = self.client.post(
            reverse('basket:basket_update'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '40.00'})
