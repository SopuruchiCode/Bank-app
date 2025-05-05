from django.shortcuts import render,redirect
from django.http import JsonResponse
from openaccount.models import Account
from .forms import DepositForm,WithdrawalLog,DepositLog
import json

def deposit_page(request):
    context = {}
    if not((request.user).is_authenticated):
        return redirect("/")
    user = request.user
    if request.method == "POST":
        form = DepositForm(request.POST)
        context["form"] = form
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            depositor_first_name = cleaned_data.get("depositor_first_name")
            depositor_last_name = cleaned_data.get("depositor_last_name")
            account_number = cleaned_data.get("account")
            coupon_code = cleaned_data.get("code")

            account = Account.objects.get(account_number=account_number)
            witdrawal_log = WithdrawalLog.objects.get(coupon_code=coupon_code)
            amount_deposited = witdrawal_log.amount
            account.deposit(coupon_code,depositor_first_name,depositor_last_name)
            account.save()
            data = {}
            data["amount-deposited"] = amount_deposited
            context["data"] = json.dumps(data)
        context["form"] = DepositForm()
    else:
        context["form"] = DepositForm()
    
    return render(request,'deposit/deposit.html',context)

    