from django.shortcuts import get_object_or_404, render
from .models import Category, Product

#Function that returns products on the index page
def product_all(request):
    products = Product.products.all()
    return render(request, 'store/index.html', {'products': products})
#Function that returns a single product when a customer views it
#Shows the product image, price, and quantity
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/single.html', {'product': product})

#Function that shows the category list on the index page of the website.
def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(category=category)
    return render(request, 'store/category.html', {'category': category, 'products': products})
