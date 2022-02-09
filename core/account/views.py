from django.contrib.auth import login, logout
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from .forms import RegistrationForm, UserEditForm
from .token import account_activation_token
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import get_template
from orders.views import user_orders, delivery_orders
from .models import UserBase
from orders.forms import ReviewAdd
from orders.models import ProductReview, Order

#Function that logs the user into their dashboard and requires a login 
#Login depends on account type for user vs driver. User will be directed to a different dashboard than driver. 
@login_required
def dashboard(request):
    if (request.user.is_driver):
        orders = delivery_orders(request)
        return render(
            request,
            "account/dashboard/driver_dashboard.html",
            {"orders": orders},
        )
    else:
        orders = user_orders(request)
        reviewForm = ReviewAdd()
        return render(
            request,
            "account/dashboard/dashboard.html",
            {"orders": orders, "form": reviewForm},
        )

#Function that lets user edit their information from the edit form in the forms.py file. 
@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(
        request, "account/dashboard/edit_details.html", {"user_form": user_form}
    )

#Function that lets users delete their account, however account is not deleted in the database, it is set as inactive 
@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")

#Function that sets up the registration functionality and sends the user an email once they have created an account with GBD.
def account_register(request):

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(
                request,
                "account/registration/register_email_confirm.html",
                {"form": registerForm},
            )

    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})

#Function that activates the account once the user clicks the link that is sent in the account confirmation email. 
def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


#Function that saves reviews into the database once customer submits on a completed order.
def save_review(request, oid):
    order = Order.objects.get(pk=oid)
    user = request.user

    if request.method == "POST":
        print("request method is post")
        form = ReviewAdd(request.POST)

        for field in form:
            print("Field Error:", field.name,  field.errors)

        print(form.is_valid())
        if form.is_valid():
            print("form is valid")
            review = form.save(commit=False)
            review.user = user
            review.order = order
            review.save()
            return redirect("account:dashboard")
        else:
            form = ReviewAdd()

    return redirect("account:dashboard")

#Sources Used
#https://docs.djangoproject.com/en/3.2/topics/http/views/
#https://www.youtube.com/watch?v=TblSa29DX6I
#https://djangobook.com/mdj2-django-views/