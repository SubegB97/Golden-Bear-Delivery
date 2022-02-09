from django.apps import AppConfig

#Makes the payment application ready to be utilized by the application. 
class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
