from django.db import models
from django.db.models import CASCADE
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse('shopping:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=CASCADE)
    in_stock = models.IntegerField()
    slug = models.SlugField(max_length=255)

    def get_absolute_url(self):
        return reverse('shopping:product_detail', args=[self.slug])

    def __str__(self):
        return self.product_name




