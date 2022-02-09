from django.apps import AppConfig

#Class that lets the orders app integrated with the application 
class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
