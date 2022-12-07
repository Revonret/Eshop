from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    categories = models.ForeignKey(Category, on_delete=CASCADE)
    in_stock = models.IntegerField()
    slug = models.SlugField(max_length=255)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    users = models.ForeignKey(User, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    product_list = models.ManyToManyField(Product)


class ProductInCart(models.Model):
    products = models.ForeignKey(Product, on_delete=CASCADE)
    carts = models.ForeignKey(Cart, on_delete=CASCADE)
    amount = models.IntegerField()


class Order(models.Model):
    product_list = models.ManyToManyField(Product),
    users = models.ForeignKey(User, on_delete=CASCADE)
    created_data = models.DateTimeField(auto_now_add=True)


class ProductsInOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE)
    orders = models.ForeignKey(Order, on_delete=CASCADE)
    amount = models.IntegerField()


