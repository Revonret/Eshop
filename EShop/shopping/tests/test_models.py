from user.models import UserBase
from django.test import TestCase
from django.urls import reverse

from shopping.models import Category, Product


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')

    def test_category_url(self):
        data = self.data1
        response = self.client.post(
            reverse('shopping:category_list', args=[data.slug]))
        self.assertEqual(response.status_code, 200)


class TestProductsModel(TestCase):
    def setUp(self):
        a = Category.objects.create(name='django', slug='django')
        UserBase.objects.create(user_name='admin')
        self.data1 = Product.objects.create(category=a, product_name='django beginners', in_stock=5,
                                            slug='django-beginners', price='20.00', description='testtesttest')
        self.data2 = Product.objects.create(category=a, product_name='django advanced', in_stock=2,
                                            slug='django-advanced', price='20.00', description='testtesttesttest')

    def test_products_model_entry(self):

        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')

    def test_products_url(self):
        data = self.data1

        url = reverse('shopping:product_detail', args=[data.slug])
        self.assertEqual(url, '/item/django-beginners/')
        response = self.client.post(
            reverse('shopping:product_detail', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

    def test_products_custom_manager_basic(self):
        data = Product.objects.all()
        self.assertEqual(data.count(), 2)
