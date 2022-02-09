from django.apps import AppConfig

#creates functionality for the account application in the project
class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
