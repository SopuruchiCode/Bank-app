from django import forms
from .models import EpaymentSubscription,PRICE_OF_KEY_PER_DAY,DJANBANK_ACCOUNT_MODEL
from openaccount.models import WithdrawalLog,Account,InsufficientbalanceError,WrongPinError
from math import ceil


class KeyPaymentForm(forms.ModelForm):
    
    choices = [
    ("Coupon", "Coupon"),
    ("Transfer", "Transfer")
]

    price = forms.DecimalField(max_digits=50,decimal_places=2,initial=PRICE_OF_KEY_PER_DAY,widget=forms.NumberInput(attrs={'readonly': True,'placeholder':'Price'}))
    payment_type = forms.ChoiceField(choices=choices, widget=forms.RadioSelect(attrs={'class':'payment-options'}))
    coupon_code = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class':'coupon-code acc-details0', 'placeholder': 'Coupon Code'}))
    account_number = forms.CharField(max_length=8,min_length=8,required=False, widget=forms.TextInput(attrs={'class': 'acc-no acc-details1', 'placeholder': 'Account Number'}))
    pin = forms.CharField(min_length=4,max_length=100,required=False, label='PIN', widget=forms.TextInput(attrs={'class': 'pin acc-details1', 'placeholder': 'PIN'}))

    class Meta:
        model = EpaymentSubscription
        fields = ['entity_name','duration', 'merchant_account']
        widgets = {
            'entity_name' : forms.TextInput(attrs={'class':'entity-name', 'placeholder':'Entity Name'}),
            'duration' : forms.NumberInput(attrs={'class':'duration', 'placeholder':'Duration'}),   
        }
        labels = {
            "duration" : 'Duration (Days)'
        }

    def __init__(self,user,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['duration'].initial = 1
        self.fields['payment_type'].initial = 'Coupon'
        self.fields['merchant_account'].queryset = Account.objects.filter(client=user)
    
        self.fields['account_number'].disabled = True
        self.fields['pin'].disabled = True
        if 'account_number' in self.data:
            self.fields['account_number'].disabled = False
            self.fields['pin'].disabled = False
            self.fields['coupon_code'].disabled = True

        

    def clean_account_number(self):
        account = self.cleaned_data.get("account_number")
        if account:
            if not Account.objects.filter(account_number=account).exists():
                raise forms.ValidationError('Invalid Account details')
            return account
        return None

    def clean_duration(self):
        duration = self.cleaned_data.get("duration")
        if duration <= 0:
            raise forms.ValidationError("Duration can't be less than 1 day")
        if ceil(duration) != duration:
            raise form.validationError('Please duration days is meant to be a whole number')
        return duration

    def clean_coupon_code(self):
        code = self.cleaned_data.get("coupon_code")

        if code:
            if not WithdrawalLog.objects.filter(coupon_code=code).exists():
                raise forms.ValidationError("Coupon is invalid")
            coupon = WithdrawalLog.objects.get(coupon_code=code)
            if coupon.redeemed:
                raise forms.ValidationError('Coupon is invalid')
            return code
        else:
            return None
            
    def clean(self):
        cleaned_data = super(KeyPaymentForm,self).clean()
        total_price = PRICE_OF_KEY_PER_DAY * cleaned_data.get('duration')

        coupon_code = cleaned_data.get("coupon_code")
        account = cleaned_data.get("account_number")
        pin = cleaned_data.get("pin")
        entity = cleaned_data.get('entity_name')

        if coupon_code:
            coupon = WithdrawalLog.objects.get(coupon_code=coupon_code)
            if coupon.amount < total_price or coupon.amount > total_price:
                raise forms.ValidationError('Coupon value does not match price to be paid')
            DJANBANK_ACCOUNT_MODEL.deposit(code=coupon_code,depositor_first_name=entity,depositor_last_name=entity)
            
        elif (account and pin):
            account = Account.objects.get(account_number=account)
            if not pin:
                raise forms.ValidationError('PIN needs to be specified for transfers')
            try:
                account.transfer_to(DJANBANK_ACCOUNT_MODEL,total_price,pin)
            except InsufficientbalanceError:
                raise forms.ValidationError("Insufficient balance")
            
            except WrongPinError:
                raise forms.ValidationError("Wrong PIN")

            except Exception:
                raise forms.ValidationError('Wassup uh an error occured')
        else:
            raise forms.ValidationError('No payment details specified')
        return self.cleaned_data

    def save(self):
        model = super(KeyPaymentForm,self).save()

class payment_gateway_form(forms.Form):
    account_number = forms.CharField(max_length=8, widget= forms.TextInput(attrs={"placeholder" : "Account Number"}))
    pin = forms.CharField(max_length=4, widget= forms.TextInput(attrs={"placeholder" : "PIN"}))

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        if account_number and Account.objects.filter(account_number=account_number).exists():
            self.cleaned_data['account_model'] = Account.objects.get(account_number=account_number)
            return account_number
            
        else:
            raise forms.ValidationError('Invalid Credentials')

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        if not (pin.isnumeric()):
            raise forms.ValidationError('Invalid Credentials')
        return pin

    def clean(self):
        cleaned_data = super().clean()
        account_model = cleaned_data.get('account_model')
        pin = cleaned_data.get('pin')
        if account_model and pin:
            if account_model.pin != pin:
                raise forms.ValidationError('Invalid Credentials')
            return cleaned_data
            