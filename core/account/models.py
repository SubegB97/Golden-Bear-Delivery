from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect

#Database model made with classes
#This class creates the superuser or admin to access the backend area of the website. 
#Super user has all access to permissions and set permissions for the dirvers. 
class CustomAccountManager(BaseUserManager):
    #Function that creates the super user
    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, user_name, password, **other_fields)
    #Function that creates the regular user for the site
    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

#This is the class is the database for regular users ("customers"). 
#Includes fields such as email, username, first & last name, country, phone number, address, town & city
class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_("email address"), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_("about"), max_length=500, blank=True)
    # Delivery details
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]
    
    #Names the database account in the admin backend area. 
    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
    
    #Function to send the email to the user which is utilized in the other view files.
    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            "goldenbeardelivery@outlook.com",
            [self.email],
            fail_silently=False,
        )
    #Dunder string method 
    def __str__(self):
        return self.user_name

#Sources used
#https://docs.djangoproject.com/en/3.2/intro/tutorial02/
#https://stackoverflow.com/questions/32744188/django-models-and-views
#https://www.youtube.com/watch?v=r9kT-jm136Q
#https://docs.djangoproject.com/en/3.2/topics/email/

