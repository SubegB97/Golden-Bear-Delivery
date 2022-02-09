
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from store.models import Product
from .cart import Cart

#Function that returns the cart summary when user adds items to the cart
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/summary.html', {'cart': cart})

#Function that adds items to the cart and displays the product and quantity
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)
        
        cartqty = cart.__len__()
        response = JsonResponse({'qty': cartqty})
        return response

#Function that removes items from teh cart once user hits remove item
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)
        
        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttotal})
        return response 
#Function that updates the cart price if user decides to increase the quantity of an item in the cart 
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update(product=product_id, qty=product_qty)

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttotal})
        return response


#Sources Used
#http://www.protutorialplus.com/django-shopping-cart
#https://docs.djangoproject.com/en/3.2/ref/request-response/