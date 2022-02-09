from django.urls import path

from . import views

app_name = "payment"

#URL routing for the payment application 
urlpatterns = [
    path("", views.CartView, name="cart"),
    path("process-payment/", views.payment_details, name="process_payment"),
    path("orderplaced/", views.order_placed, name="order_placed"),
    path("webhook/", views.stripe_webhook),
]
