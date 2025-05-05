from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db.models import Q
from openaccount.models import WithdrawalLog,transfer_logs,Account,DepositLog
import json


# Create your views here.
def history_acc_display(request):           #for javascript to send account to be displayed   (Is this an API? future me.)
    if request.method == "POST":
        print(request.body)
        account_displayed = json.loads(request.body)
        temp = account_displayed["account-displayed"]
        request.session["accountNo_displayed"] = temp
        
    return JsonResponse({"status":"success"})


   
    # credit_logs = []
    # debit_logs = []
    # logs = []
    # logs_between_user_accounts = []
    # user = request.user
    # user_accounts = Account.objects.filter(client=user)
    # context["accounts"] = user_accounts

    # transfers = transfer_logs.objects

    # for i in user_accounts:
    #     user_accounts_transfer_to = transfers.filter(Q(sender=i.account_number) | Q(recepient=i.account_number))
    #     if len(user_accounts_transfer_to) != 0:
    #         for j in user_accounts_transfer_to:
    #             if (user_accounts.filter(account_number=j.sender)) and (user_accounts.filter(account_number=j.recepient)):  
    #                 #to retrieve logs that were transfered between the user accounts
    #                 logs_between_user_accounts.append(j)
    #             else:
    #                 logs.append(j)

    # context["logs"] = logs
    # context["nonadding"] = logs_between_user_accounts
    # print(logs_between_user_accounts)


def history_page(request):
    context = {}
    data = {}
    if not request.user.is_authenticated:
        return redirect("/")
        
    user_accounts = Account.objects.filter(client=request.user)
    list_of_accounts = []

    for _ in user_accounts:
        list_of_accounts.append(str(_.account_number))
        data[str(_.account_number)] = []
        
    transfers = transfer_logs.objects.all()
    context["accounts"] = user_accounts

    # if request.method == "POST":
    #     for i in transfers:
    #         log_data_debit= {}
    #         log_data_credit = {}
    #         if i.sender in list_of_accounts:

    #             log_data_debit["id"] = str(i.id)
    #             log_data_debit["sender"] = str(i.sender)
    #             log_data_debit["recepient"] = str(i.recepient)
    #             log_data_debit["amount"] = str(i.amount)
    #             log_data_debit["date"] = str(i.date)
    #             log_data_debit["folio"] = "Debit"

    #             data[i.sender].append(log_data_debit)

    #         if i.recepient in list_of_accounts:

    #             log_data_credit["id"] = str(i.id)
    #             log_data_credit["sender"] = str(i.sender)
    #             log_data_credit["recepient"] = str(i.recepient)
    #             log_data_credit["amount"] = str(i.amount)
    #             log_data_credit["date"] = str(i.date)
    #             log_data_credit["folio"] = "Credit"

    #             transfer_data[i.recepient].append(log_data)
    #     print(request.body)
    #     return JsonResponse(transfer_data)               # for the JavaScript code

    return render(request,"history/history.html",context)

"""{
    account-number:
    
    [{      log_id:"",
            sender:"",
            recepient:"",
            amount:"",
            date:"",
            credit:""
        }]
}"""

def transfer_history(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error":"Invalid Request(User is not authenticated)"})

    transfer_data = {}        
    user_accounts = Account.objects.filter(client=request.user)
    list_of_accounts = []

    for _ in user_accounts:
        list_of_accounts.append(str(_.account_number))
        transfer_data[str(_.account_number)] = []
        
    transfers = transfer_logs.objects.all()

    if request.method == "POST":
        for i in transfers:
            log_data_debit= {}
            log_data_credit = {}

            if i.sender in list_of_accounts:
                log_data_debit["id"] = str(i.id)
                log_data_debit["sender"] = str(i.sender)
                log_data_debit["recepient"] = str(i.recepient)
                log_data_debit["amount"] = str(i.amount)
                log_data_debit["date"] = str(i.date)
                log_data_debit["folio"] = "Debit"

                transfer_data[i.sender].append(log_data_debit)

            if i.recepient in list_of_accounts:
                log_data_credit["id"] = str(i.id)
                log_data_credit["sender"] = str(i.sender)
                log_data_credit["recepient"] = str(i.recepient)
                log_data_credit["amount"] = str(i.amount)
                log_data_credit["date"] = str(i.date)
                log_data_credit["folio"] = "Credit"

                transfer_data[i.recepient].append(log_data_credit)
        print(request.body)
        return JsonResponse(transfer_data)               # for the JavaScript code

    else:
        return JsonResponse({"error":"Invalid Request"})

"""{
    account-number:
    
    {"unclaimed":[{      log_id:"",
            amount:"",
            coupon_code:"",
            redeemed:"",
            date:""
        }]
    
    "claimed":[{      log_id:"",
            amount:"",
            coupon_code:"",
            redeemed:"",
            date:""
        }]
    }
}"""
def withdrawal_history(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error":"Invalid Request(User is not authenticated)"})

    if request.method == "POST":
        withdraw_data = {}
        list_of_accounts = []
        user_accounts = Account.objects.filter(client=request.user)

        for _ in user_accounts:
            withdraw_data[str(_)] = {}
            withdraw_data[str(_)]["unclaimed"] = []
            withdraw_data[str(_)]["claimed"] = []
            list_of_accounts.append(str(_.account_number))

        withdrawal_logs = WithdrawalLog.objects.filter(account_no__in=list_of_accounts)

        for log in withdrawal_logs:
            log_data = {}
            log_data["id"] = str(log.id)
            log_data["amount"] = log.amount
            log_data["coupon_code"] = str(log.coupon_code)
            log_data["date"] = str(log.date)

            if log.redeemed == True:
                log_data["redeemed"] = "Yes"
                withdraw_data[str(log.account_no)]["claimed"].append(log_data)
            else:
                log_data["redeemed"] = "No"
                withdraw_data[str(log.account_no)]["unclaimed"].append(log_data)
        print(request.body)
        return JsonResponse(withdraw_data)
    else:
        return JsonResponse({"error":"Invalid Reponse"})
    
'''
{
account-number: [
    {   
        log-id:
        first-name:
        last-name:
        amount: 
        date:
    }
]


}
'''
def deposit_logs(request):
    data = {}
    list_of_accounts = []
    account_deposit_logs = []
    if request.method == "POST":
        user = request.user
        user_accounts = Account.objects.filter(client=user)
        for acc in user_accounts:
            list_of_accounts.append(acc.account_number)
            data[acc.account_number] = []

        raw_deposit_logs = DepositLog.objects.all()
        for log in raw_deposit_logs:
            if log.account in list_of_accounts:
                account_deposit_logs.append(log)
                log_data = {}
                log_data["id"] = log.id
                log_data["depositor-name"] = f"{log.depositor_first_name} {log.depositor_last_name}"
                log_data["amount"] = log.amount
                log_data["date"] = log.date
                data[log.account].append(log_data)
        bodybytes = request.body
        body = bodybytes.decode("utf-8")
        body = json.loads(body)
        print(body)
        return JsonResponse(data)
    return JsonResponse({"Error": "Invalid request "})