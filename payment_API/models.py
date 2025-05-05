from django.db import models,IntegrityError
from string import digits,ascii_letters
from random import choices
from datetime import datetime,timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from openaccount.models import Account


USERMODEL = get_user_model()
PRICE_OF_KEY_PER_DAY = 200.00
DJANBANK_ACCOUNT_MODEL = Account.objects.get(account_number="44996971")
DJAN_PIN = DJANBANK_ACCOUNT_MODEL.pin

def keyGenerator(length=30) -> str:
    return ''.join(choices((digits+ascii_letters),k=length))


class EpaymentSubscription(models.Model):
    api_key = models.CharField(max_length=50,default=keyGenerator, unique=True)
    merchant_account = models.ForeignKey(Account, models.CASCADE,null=True)
    price_per_day = models.DecimalField(decimal_places=2,max_digits=10,default=PRICE_OF_KEY_PER_DAY)
    entity_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.now)
    expiry_date = models.DateTimeField()
    duration = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.api_key

    def check_if_active(self):
        return self.is_active

    def save(self):
        
        if self.duration <= 0:
            raise ValidationError('Duration must be more than zero')
        if self.expiry_date == ("" or None):
            self.expiry_date = self.start_date + timedelta(days=self.duration)
        
        # if self.expiry_date < datetime.now():
        #     self.is_active = False

        tries = 0
        while tries < 5:
            try:
                return super(EpaymentSubscription,self).save()
            except IntegrityError:
                self.api_key = keyGenerator()
                tries += 1
                if tries == 5:
                    return IntegrityError(" Non Unique API key")


class Transaction_detail(models.Model):
    client_id = models.CharField(max_length=30)
    merchant_id = models.ForeignKey(EpaymentSubscription,on_delete=models.SET_NULL, null=True)
    transaction_id_client = models.CharField(max_length=30, unique=True)
    amount = models.DecimalField(max_digits=15,decimal_places=2)
    callback_code = models.CharField(max_length=16)
    callback_url = models.TextField()

    def __str__(self):
        return f'{self.id}'
    
class PaymentLogging(models.Model):
    merchant_id = models.ForeignKey(EpaymentSubscription,on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=15,decimal_places=2)
    processing_fee = models.DecimalField(max_digits=15,decimal_places=2)
    client = models.ForeignKey(Account,on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.id}'

    
# class LogPayment