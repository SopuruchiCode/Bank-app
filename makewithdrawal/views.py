from django.shortcuts import render,redirect
from django.http import JsonResponse
from openaccount.models import WithdrawalLog
from .forms import WithdrawalForm
from openaccount.models import Account
import json
from time import sleep

def newest_coupon_code(request):
    if request.method == "POST":
        print(request.body)
        response = request.session.get("withdraw-app")
        if response:
            print(response)
            response = response.get("newest-withdrawal")
            print(response)
            return JsonResponse(response)
    else:
        return None

def withdrawal_page(request):
    total_data = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("/")

    context = {}
    form = WithdrawalForm(user=user)
    withdraw_data = {}

    if request.method == "POST":
        form_validity = False
        if not request.POST:
            return JsonResponse({"error":"Empty body"},status=400)
            
        form = WithdrawalForm(user,request.POST)
        context["form"] = form

        if form.is_valid():
            form_validity = True
            data = form.cleaned_data
            form = WithdrawalForm(user=user)
            context["form"] = form
            account = data.get("account_no")
            amount = data.get("amount")
            pin = data.get("pin")

            coupon_code = account.withdraw(amount,pin)  
            withdraw_data["account"] = str(account)
            withdraw_data["amount"] = amount
            withdraw_data["coupon"] = coupon_code
            total_data["newest-withdrawal"] = withdraw_data
            request.session["withdraw-app"] = total_data            #  I am saving it in this format to prevent possible naming conflicts

        else:
            form_errors = form.errors
            print(form_errors)
        
        if "application/json" not in request.headers.get("Accept",""):
            return render(request,"withdrawal/withdrawal.html",context)

        elif "application/json" in request.headers.get("Accept",""):              #Checking if fetch request
            if not form_validity:
                return JsonResponse({"status":"error","errors":form_errors})
            return JsonResponse({"status":"success","coupon-code" : coupon_code})# Future me, remember to implement that idea of using the rsa file to encrypt this data


            # -------------------------------------------------------------------------- old attempt    \|/ down below  
            # if not request.body:
            #     return JsonResponse({'error':"empty request body"},status=400)
            # try:
            #     body_unicode = request.body.decode("utf-8")
            #     body_data = json.loads(body_unicode)
            #     print(body_data,"body")
            # except json.JSONDecodeError:
            #     return JsonResponse({"error":"Invalid JSON data"})

            # if body_data:
            #     # account = Account.objects.filter(account_number = body_data.get("account"))
            #     # amount = body_data.get("amount")
            #     # pin = body_data.get("pin")
            #     form = WithdrawalForm(user,body_data)

            #     if form.is_valid():
            #         print("YES")
            #     return JsonResponse(withdraw_data)
            # else:
            #     return JsonResponse({'error':'Wrong Request'},status=400)

                
    if request.method == "GET":
        context["form"] = form
        return render(request,"withdrawal/withdrawal.html",context)