from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'description', 'category', 'in_stock', 'slug']
    list_filter = ['product_name']
    list_editable = ['price', 'in_stock']
