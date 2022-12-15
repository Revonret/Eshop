from importlib import import_module
import pytest

from django.conf import settings
from user.models import UserBase
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from shopping.models import Category, Product
from shopping.views import shop


class PageTests(TestCase):
    def test_home(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        UserBase.objects.create(user_name='admin')
        a = Category.objects.create(name='django', slug='django')
        Product.objects.create(category=a, product_name='django beginners', in_stock=5,
                               slug='django-beginners', price='20.00', description='testtesttest')

    def test_url_allowed_hosts(self):

        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='127.0.0.1:8000')
        self.assertEqual(response.status_code, 400)

    def test_homepage_url(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_url(self):
        response = self.c.get(
            reverse('shopping:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.c.get(
            reverse('shopping:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = shop(request)
        html = response.content.decode('utf8')
        self.assertIn('Home', html)
        self.assertEqual(response.status_code, 200)
