from .cart import Cart

#Function that returns the cart when it is requested on the browser 
def cart(request):
    return {'cart': Cart(request)}