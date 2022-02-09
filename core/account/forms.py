from django import forms 
from .models import UserBase
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

#User login form that requires the username email and password to login to the website.
class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))

#User registration class that asks for user name, email, and password twice for verification. 
class RegistrationForm(forms.ModelForm):

    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)
    
    #Meta class that changes the field names in the backend admin area
    class Meta:
        model = UserBase
        fields = ('user_name', 'email')

    #Function that makes sure that each username is unique to the user. Will not let two users have the same username. 
    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name


    #Function to make sure that the passwords entered at registration match eachother. 
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
  
    #Function that makes sure that each username is unique to the user. Will not let two users have the same email. 
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
    
    #Function that passes an undetermined number of arguments and key-worded arguments to a class/object upon creation.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})

#Class that lets the user reset their password as long as they have an active account in the database. 
class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))
    #Function that makes sure the email entered for reset is in the database. 
    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email

#Class Form that lets the user enter a new password twice to change. 
class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

#Class Form that allows the user to edit personal information such as email, first and last name, phone number, zipcode, address, building/room and City/state. 
class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))
    
    first_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'First Name', 'id': 'form-lastname'}))
    
    phone_number = forms.CharField(
        label='Phone Number', min_length=0, max_length=15, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Phone Number', 'id': 'form-phone_number'}))
    
    postcode = forms.CharField(
        label='Zip Code', min_length=0, max_length=5, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Zip Code', 'id': 'form-postcode'}))
    
    address_line_1 = forms.CharField(
        label='Primary Address', min_length=0, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Address 1', 'id': 'form-address_line_1'}))
    
    address_line_2 = forms.CharField(
        label='Building & Room Number', min_length=0, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Building & Room #', 'id': 'form-address_line_2'}))
    
    town_city = forms.CharField(
        label='City & State', min_length=0, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'City & State', 'id': 'form-town_city'}))

    
    
    #Meta class that changes the field names in the backend admin area
    class Meta:
        model = UserBase
        fields = ('email', 'first_name', 'phone_number', 'postcode', 'address_line_1', 'address_line_2', 'town_city',)
    #Function that doesn't let the email to change once created in teh login. 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True
    


#Sources Used
#https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
#https://stackoverflow.com/questions/11923317/creating-django-forms
#https://www.thiscodeworks.com/python-creating-django-forms-stack-overflow-python/5ed033eaad58eb00148f0e36
