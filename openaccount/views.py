from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from accounts.models import CustomUser
from .models import Account
from .forms import AccountCreationForm
from string import digits
from random import choices
import json

def homepage(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        queryset_of_accounts = Account.objects.all().filter(client=user)
        account_list = []
        account_data = {}
        for acc in queryset_of_accounts:
            acc_no = str(acc)
            acc_balance = acc.amount
            account_data[acc_no] = acc_balance
            account_list.append(acc)
        request.session["account-data"] = account_data
        account_data = json.dumps(account_data)
        context["accounts"] = account_list
        context["accountData"] = account_data 

    return render(request,"home.html",context)

def account_info_view(request):
    account_data = request.session.get("account-data",{})
    return JsonResponse(account_data)

def open_account(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("/")

    user = CustomUser.objects.get(bvn=str(user))
    if request.method == "POST":
        context["form"] = AccountCreationForm(user,request.POST)
        if context["form"].is_valid():
            accountInstance = context["form"].save()
            accountData  = {}
            accountData["client"] = str(accountInstance.client)
            accountData["accountNumber"] = str(accountInstance.account_number)
            accountData = json.dumps(accountData)
            context["accountData"] =  accountData

    else:
        context["form"] = AccountCreationForm(user)
        context["accountData"] = ""
        # try:
        #     user = CustomUser.objects.get(bvn=presentuser)
        #     useracc = Account.objects.filter(client=user).values()
        #     print(useracc)

        # except Exception:
        #     user = None
    return render(request,"openaccount/openaccount.html",context)

# def login(request):

#     form = LoginForm()
#     error_mess = ""
#     if request.method == "POST":
#         if request.POST:
#             form = LoginForm(request.POST)
#             if form.is_valid():
#                 clean_data = form.cleaned_data
#                 acc_no = clean_data.get("account_no")
#                 form_pin = clean_data.get("pin")

#                 customer = CustomUser.objects.filter(account_number=acc_no).values()[0]
#                 real_pin = customer.get("pin")
#                 if real_pin == form_pin:
#                     return HttpResponseRedirect(f"/logged-in/{str(acc_no)}")
                
#                 else:
#                     error_mess = "Wrong PIN or Account Number"
#         else:
#             form = LoginForm()

#     context = {"form":form,
#                "wrong_pin_message":error_mess}
#     return render(request,"openaccount/login.html",context)

# def logged_in(request,account_no):
#     customer = CustomUser.objects.filter(account_number=account_no).values()[0]
#     customer_list = CustomUser.objects.all()
    
#     cust_first_name = customer.get("first_name")
#     cust_last_name = customer.get("last_name")
#     cust_balance = customer.get("amount")
#     cust_pin = customer.get("pin")

#     context = {"name": cust_first_name,
#                "balance": cust_balance}
#     return render(request,"openaccount/logged-in-page.html",context)