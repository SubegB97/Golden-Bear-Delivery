from django.contrib import admin

from .models import UserBase

#Class that displays the admin information and account status. 
class UserBaseAdmin(admin.ModelAdmin):
    list_display = ("first_name", "email", "user_name", "is_active", "is_driver")

#registers the database model.
admin.site.register(UserBase, UserBaseAdmin)
