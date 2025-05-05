from django.shortcuts import render,redirect, reverse
from django.http import JsonResponse
from .models import PRICE_OF_KEY_PER_DAY, EpaymentSubscription, Transaction_detail, DJANBANK_ACCOUNT_MODEL,DJAN_PIN,PaymentLogging
from .forms import KeyPaymentForm,payment_gateway_form
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from json import loads
from openaccount.models import InsufficientbalanceError, WrongPinError
import requests as REQUESTS

LEVY_RATE = Decimal(0.02).quantize(Decimal('0.01'))
error_codes = {
    '0000' : 'missing payment details',
    '0001' : 'invalid merchant-id/api-key',
    '0002' : 'amount is too low',
    '1003' : 'record does not exist',
    '1004' : 'invalid/missing credentials'
}

def API_key_is_valid(key):
    return EpaymentSubscription.objects.filter(api_key=key).exists()

def transaction_detail_exists(client_id, merchant_id, transaction_id):
    if API_key_is_valid(merchant_id):
        merchant_id = EpaymentSubscription.objects.get(api_key=merchant_id)
        return (Transaction_detail.objects.filter(client_id=client_id,merchant_id=merchant_id,transaction_id_client=transaction_id).exists()) and (len(Transaction_detail.objects.filter(client_id=client_id,merchant_id=merchant_id,transaction_id_client=transaction_id)) == 1)
    else:
        return None
    
def key_payment_page(request):
    if not request.user.is_authenticated:
        return redirect('/')
    context = {}
    form = KeyPaymentForm(user=request.user)
    if request.method == "POST":
        form = KeyPaymentForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            form = KeyPaymentForm(user=request.user)
                
    context["form"] = form
    return render(request, "payment_api/keypayment.html", context)

@csrf_exempt
def get_current_price(request):
    if request.method != 'POST':
        return JsonResponse({'error' : 'Bad Request'})
    data = {
        'price-per-day' : PRICE_OF_KEY_PER_DAY
    }
    
    return JsonResponse(data)

def payment_result_page(request):
    status = request.session.get('payment_status', None)
    error_code = request.session.get('eid', None)
    if status == 'success':
        return render(request, 'payment_api/success.html' )
    elif status == 'failure' and error_code:
        context = {'eid' : error_code}
        return render(request, 'payment_api/error.html', context )
    else:
        return redirect('/')

@csrf_exempt
def payment_gateway_page(request):
    context = {}
    form = payment_gateway_form()

    if request.method == 'GET':
        client_id = request.GET.get('client-id', None)
        merchant_id = request.GET.get('merchant-id', None)
        transaction_id = request.GET.get('transaction-id', None)

        if not(client_id and merchant_id and transaction_id) or not (API_key_is_valid(merchant_id)) or not (transaction_detail_exists(client_id=client_id,merchant_id=merchant_id,transaction_id=transaction_id)):
            # context['eid'] = '1004'
            # return render(request, 'payment_api/error.html', context)

            request.session['eid'] = '1004'
            request.session['payment_status'] = 'failure'
            return redirect(reverse(payment_result_page))
        try:
            if merchant_id:
                merchant_id = EpaymentSubscription.objects.get(api_key=merchant_id)
            transaction_details = Transaction_detail.objects.get(client_id=client_id,merchant_id=merchant_id,transaction_id_client=transaction_id)
        except Exception:
            # context['eid'] = '1003'
            # return render(request, 'payment_api/error.html', context)

            request.session['eid'] = '1003'
            request.session['payment_status'] = 'failure'
            return redirect(reverse(payment_result_page))
        
    if request.method == 'POST':
        if request.headers.get('type-of-request') == 'transaction-details':
            data = loads(request.body)
            client_id = data.get('client-id', None)
            merchant_id = data.get('merchant-id', None)
            transaction_id = data.get('transaction-id', None)
            amount = data.get('amount', None)
            callback_url  = data.get('callback-url', None)
            callback_code = data.get('callback-code', None)


            if not (client_id and merchant_id and transaction_id and amount and callback_code and callback_url):
                return JsonResponse(data= {'error' : '0000'}, status=400)
            
            if not API_key_is_valid(merchant_id):
                return JsonResponse(data= {'error' : '0001'}, status=400)    
            
            if amount:
                amount = Decimal(amount).quantize(Decimal('0.01'))
                if amount < 100:
                    return JsonResponse(data= {'error' : '0002'}, status=400)
            if merchant_id:
                merchant_id = EpaymentSubscription.objects.get(api_key=merchant_id)

            try:       
                Transaction_detail.objects.create(client_id=client_id, merchant_id=merchant_id, transaction_id_client=transaction_id, amount=amount,callback_code=callback_code, callback_url=callback_url)
            
            except Exception as e:
                print(e)
                return JsonResponse(data= {'error' : '0003'}, status=400)
            
            return JsonResponse({'status' : 'recieved'},status=200)

        else:
            form = payment_gateway_form(request.POST)
            if form.is_valid():
                print('io: form is valid')

                client_id = request.GET.get('client-id', None)
                merchant_id = request.GET.get('merchant-id', None)
                transaction_id = request.GET.get('transaction-id', None)

                if not(client_id and merchant_id and transaction_id) or not (API_key_is_valid(merchant_id)) or not (transaction_detail_exists(client_id=client_id,merchant_id=merchant_id,transaction_id=transaction_id)):
                    # context['eid'] = '1004'
                    # return render(request, 'payment_api/error.html', context)

                    request.session['eid'] = '1004'
                    request.session['payment_status'] = 'failure'
                    return redirect(reverse(payment_result_page))

                try:
                    if merchant_id:
                        merchant_id = EpaymentSubscription.objects.get(api_key=merchant_id)
                    transaction_details = Transaction_detail.objects.get(client_id=client_id,merchant_id=merchant_id,transaction_id_client=transaction_id)

                except Exception:
                    context['eid'] = '1003'
                    return render(request, 'payment_api/error.html', context)
                
                else:
                    amount = Decimal(transaction_details.amount).quantize(Decimal('0.01'))
                    levy = Decimal(LEVY_RATE * amount).quantize(Decimal('0.01'))
                    actual_amt = Decimal(amount - levy).quantize(Decimal('0.01'))

                    form_data = form.cleaned_data
                    acc_model = form_data.get('account_model')
                    merchant_account = merchant_id.merchant_account
                    pin = form_data.get('pin')
                    print('io: else is valid')


                    try:
                        acc_model.transfer_to(DJANBANK_ACCOUNT_MODEL,float(amount),pin)
                        DJANBANK_ACCOUNT_MODEL.transfer_to(merchant_account,float(actual_amt),DJAN_PIN)
                        PaymentLogging.objects.create(client=acc_model,merchant_id=merchant_id, amount=amount, processing_fee=levy)

                        
                        print('io: money has been transferred...')

                    except InsufficientbalanceError as e:
                        # context['eid'] = 'Insufficient Balance'
                        # return render(request, 'payment_api/error.html', context)

                        request.session['eid'] = 'Insufficient Balance'
                        request.session['payment_status'] = 'failure'
                        print(e)
                        return redirect(reverse(payment_result_page))


                    except WrongPinError as e:
                        # context['eid'] = 'Invalid Credentials'
                        # return render(request, 'payment_api/error.html', context)

                        request.session['eid'] = 'Invalid Credentials'
                        request.session['payment_status'] = 'failure'
                        print(e)
                        return redirect(reverse(payment_result_page))


                    else:
                        print('io: payment-successful')
                        payload = {
                            'status' : 'success',
                            'callback-code' : f'{transaction_details.callback_code}',
                            'client-id' : f'{transaction_details.client_id}',
                            'transaction-id' : f'{transaction_details.transaction_id_client}',
                            'api-key' : str(transaction_details.merchant_id)

                        }
                        response = REQUESTS.post(url= transaction_details.callback_url, json=payload)
                        request.session['payment_status'] = 'success'
                        return redirect(reverse(payment_result_page))
                
    context['form'] = form
    return render(request, 'payment_api/payment-gateway.html',context)