import json
import os
import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings
from cart.cart import Cart
from orders.views import payment_confirmation

#Class that takes user to an error page if their card does not work.
class Error(TemplateView):
    template_name = "payment/error.html"

#Function that shows the customer their cart, they must be logged in.
@login_required
def CartView(request):

    cart = Cart(request)
    total = str(cart.get_total_price())
    total = total.replace(".", "")
    total = int(total)
    print(total)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total, currency="gbp", metadata={"userid": request.user.id}
    )

    return render(
        request,
        "payment/payment_form.html",
        {
            "client_secret": intent.client_secret,
            "STRIPE_PUBLISHABLE_KEY": os.environ.get("STRIPE_PUBLISHABLE_KEY"),
        },
    )

#Function that posts the payment details once a payment is made.
@login_required
def payment_details(request):
    if request.method == "POST":
        print(request.body)

#Links up the Stripe webhook with the ordering 
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    print("stripe webhook activated")

    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == "payment_intent.succeeded":
        print(event.data)
        payment_confirmation(event.data.object.client_secret)

    else:
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)

#Function that clears the cart once the order is placed.
def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "payment/orderplaced.html")

#Sources
#https://docs.djangoproject.com/en/3.2/ref/csrf/
#https://www.youtube.com/watch?v=WCEi4sTVjH4

