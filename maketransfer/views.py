from django.shortcuts import render,redirect
from django.http import JsonResponse
from .forms import TransferForm
from openaccount.models import Account
from django.core.exceptions import ValidationError
import json

def acc_info(request):
    account_data = request.session.get("account-data",{})
    return JsonResponse(account_data)


def transfer(request):
    errors = []
    context = {"success":""}
    context_err = {}

    if not request.user.is_authenticated:
        return redirect("/")
    
    queryset_of_accounts = Account.objects.all().filter(client=request.user)
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

    if request.method == "POST":
        context["form"] = TransferForm(request.user,request.POST)
        if context["form"].is_valid():
            try:
                transfer_data = context["form"].cleaned_data
                rec_acc1 = transfer_data["rec_account"]
                rec_acc = Account.objects.get(account_number=rec_acc1)
                sender_acc = transfer_data.get("acc_of_sender")
                amount = transfer_data.get("amount")
                pin = transfer_data.get("pin")

            except Exception as e:
                context_err["errors"] = f"{rec_acc1} account does not exist"
                return render(request, "transfer/transfer-errors.html", context_err)

            try:
                sender_acc.transfer_to(rec_acc,amount,pin)
                context["form"] = TransferForm(request.user)
                context["success"] = "success"

            
            except ValidationError as e:
                errors += list(e)
                context_err["errors"] = errors
                return render(request, "transfer/transfer-errors.html", context_err)

    else:
        context["form"] = TransferForm(request.user)

    return render(request,"transfer/transfer.html",context)