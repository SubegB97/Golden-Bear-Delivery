from store.models import Product
from decimal import Decimal
from django.conf import settings

#A base Cart class, providing some default behaviors that can be inherited or overrided, as necessary
class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Function that has adding and updating functionality in the users cart session data
    def add(self, product, qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()

    #Function that collects the product_id in the session data to query the database and return products
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
    
    #Function that gets the basket data and count the qty of items
    def __len__(self):
        
        return sum(item['qty'] for item in self.cart.values())
    
    #Function that updates values in the session data
    def update(self, product, qty):
        product_id = str(product) 
        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        self.save()

    #Function that gets the total price of the cart and shows it to the customer. 
    def get_total_price(self):

        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(1.50)

        total = subtotal + Decimal(shipping)
        return total


    #Function that deletes items from session data
    def delete(self, product):
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]
            print(product_id)
            self.save()
  
    #Function that removes the basket from the session.
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    #Function that saves the session. 
    def save(self):
        self.session.modified = True
    

    #Sources Used 
    #https://django-shop.readthedocs.io/en/latest/reference/cart-checkout.html
    #https://stackoverflow.com/questions/36147597/adding-items-to-shopping-cart-django-python
    #https://docs.djangoproject.com/en/3.2/topics/http/sessions/
    #https://www.youtube.com/watch?v=HYOvEIimVzI
    
        
   

    