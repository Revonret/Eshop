from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def shop(request):
    products = Product.products.all()
    return render(request, 'home.html', {'products': products})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shopping/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shopping/detail.html', {'product': product})
