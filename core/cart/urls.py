from django.urls import path 

from . import views 

app_name = 'cart'

#Url routing paths for the cart application. 
urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('add/', views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('update/', views.cart_update, name='cart_update'),
]

#Sources Used
#https://docs.djangoproject.com/en/3.2/topics/http/urls/
#https://www.youtube.com/watch?v=TblSa29DX6I