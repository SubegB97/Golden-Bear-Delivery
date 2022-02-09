from django.contrib import admin

from .models import Order, OrderItem, ProductReview

""" admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductReview) """

#Class that displays these fields for admin (Owner) in the admin backend area once a customer completes an order
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "address1",
        "address2",
        "state",
        "phone",
        "total_paid",
        "billing_status",
        "delivery_status",
    )
    list_filter = ("billing_status", "created", "updated")


admin.site.register(Order, OrderAdmin)

#Class that displays the order items in the admin backend area
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "price",
        "quantity",
    )


admin.site.register(OrderItem, OrderItemAdmin)

#Class that shows the admin the review left by the customer after they have received an order
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "order",
        "review_text",
        "review_rating",
    )


admin.site.register(ProductReview, ProductReviewAdmin)
