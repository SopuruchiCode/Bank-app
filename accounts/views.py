from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm,CustomUser,my_login_form
from django.contrib.auth import authenticate,login
from .authentication import BvnBackend

# Create your views here.
def signup(request):
    bvn=""
    name=""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            bvn = user.bvn
            name = f"{user.first_name} {user.last_name}"

    else:
        form = CustomUserCreationForm()
    context = {"form":form,
                "bvn":bvn,
                "name":name,}
    return render(request,"registration/signup.html",context)

def my_login_view(request):
    list_of_errors = []
    context = {"errors":list_of_errors}
    if request.method == "POST":
        form = my_login_form(request.POST)
        context["form"] = form
        if form.is_valid():
            data = form.cleaned_data
            bvn = data.get("bvn")
            password = data.get("password")
            
            user = authenticate(bvn=bvn,password=password)
            if user is not None:
                if user.is_active:
                    login(request, user, backend="accounts.authentication.BvnBackend")
                    print("signed in.")
                    if user.is_staff:
                        print("superuser")
                    return HttpResponseRedirect(f"/")

                else:
                    context.get("errors").append("user is not active")
                    print("disabled account")

            else:
                context.get("errors").append("Invalid BVN or password")
                print("invalid login")
    else:
        form = my_login_form()
        context["form"] = form
    return render(request,"registration/login.html", context)