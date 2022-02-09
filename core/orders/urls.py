from django.urls import path

from . import views

app_name = "orders"

#URL routing for the orders application 
urlpatterns = [
    path("add/", views.add, name="add"),
    path("payment_confirmation/", views.payment_confirmation, name="payment_confirmation"),
]
