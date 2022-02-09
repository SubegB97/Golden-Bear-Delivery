from django.apps import AppConfig

#Registers the store application to be utilized with the rest of the project
class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
