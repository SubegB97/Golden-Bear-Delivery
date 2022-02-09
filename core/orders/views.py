from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import get_template

from cart.cart import Cart

from .models import Order, OrderItem

#Function that lets users pay for their order
#Order gets created and once payment is sucessful, user is routed to a sucuess page
def add(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":

        order_key = request.POST.get("order_key")
        name = request.POST.get("custName")
        add1 = request.POST.get("custAdd")
        add2 = request.POST.get("custAdd2")
        postCode = request.POST.get("postCode")
        phoneNumber = request.POST.get("phoneNumber")
        state = request.POST.get("state")

        user_id = request.user.id
        carttotal = cart.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name=name,
                address1=add1,
                address2=add2,
                post_code=postCode,
                phone=phoneNumber,
                state=state,
                total_paid=carttotal,
                order_key=order_key,
            )
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["qty"],
                )

        response = JsonResponse({"success": "Order payment details updated"})
        return response

#Function confirms the payment in tanget with Stripe
#If payment is successful the billing status checks true in the admin backend area. 
def payment_confirmation(request):
    if request.POST.get("action") == "post":
        order_key = request.POST.get("order_key")
        print(order_key)
        order = Order.objects.get(order_key=order_key)
        order.billing_status = True
        order.save()
        user = request.user

        # Sending order confirmation email
        current_site = get_current_site(request)
        subject = "Your Goldenbear Order has been confirmed"
        message = render_to_string(
            "payment/order_confirmation_email.html",
            {
                "order": order,
                "order_key": order_key,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            },
        )

        user.email_user(subject=subject, message=message)

    return JsonResponse({"success": "Order billing status updated"})

#Function that shows the customer their order on their dashboard once payment is successful. 
def user_orders(request):
    user_id = request.user.id
    orders = (
        Order.objects.filter(user_id=user_id)
        .filter(billing_status=True)
        .order_by("-updated")
    )
    return orders

#Shows the orders by ordering them from the oldest to most recent. 
def delivery_orders(request):
    orders = Order.objects.filter(billing_status=True).order_by("-updated")
    return orders
