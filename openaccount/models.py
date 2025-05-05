from django.db import models,IntegrityError
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from random import choices
from string import digits,ascii_letters

def generate_unique_id():
    mydigits = digits
    return ''.join(choices(mydigits,k=8))
def min_name_length(name):
    if len("".join(name.split())) < 3:
        raise ValidationError("Name is too short")

class transfer_logs(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=8)
    recepient = models.CharField(max_length=8)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.sender} transferred {self.amount} to {self.recepient}"

chars = ascii_letters + digits
LENGTH_OF_COUPON_CODE = 100

def coupon_generator(times):
    return ''.join(choices(chars,k=times))

class CouponCollision(Exception):
    pass
class InsufficientbalanceError(Exception):
    pass
class WrongPinError(Exception):
    pass

class DepositLog(models.Model):
    depositor_first_name = models.CharField(max_length=50,validators=[min_name_length])
    depositor_last_name = models.CharField(max_length=50,validators=[min_name_length],)
    account = models.CharField(max_length=8)
    amount = models.FloatField(default=None)
    code = models.CharField(max_length=500,unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self):
        self.depositor_first_name = "".join(self.depositor_first_name.split())
        self.depositor_last_name = "".join(self.depositor_last_name.split())

        if not self.amount:
            code = WithdrawalLog.objects.get(coupon_code=self.code)
            self.amount = code.amount
        
        super(DepositLog,self).save()

    def __str__(self):
        return f" Deposit log of {self.date}"


class WithdrawalLog(models.Model):
    account_no = models.CharField(max_length=8)
    amount = models.FloatField()
    redeemed = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=100,unique=True,default=None)
    date = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.coupon_code:
            self.coupon_code = coupon_generator(LENGTH_OF_COUPON_CODE)

        attempts = 0
 
        while attempts < 5:
            try:
                super(WithdrawalLog,self).save(*args,**kwargs)
                break
            except IntegrityError:
                attempts += 1
                self.coupon_code = coupon_generator(LENGTH_OF_COUPON_CODE)
                if attempts >= 5:
                    raise CouponCollision("NON UNIQUE COUPON CODE")
        return self.coupon_code
    def __str__(self):
        return f"{self.id}"  
        
class Account(models.Model):
    account_number = models.CharField(
                            primary_key = True,
                            unique=True,
                            default=generate_unique_id,
                            max_length=8,
                            editable=False
                            )
    
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    pin = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.account_number}"

    def transfer_to(self,recepient,amount,pin):
        if (self.pin == pin):
            if ((self.amount - amount) >= 0):
                self.amount = self.amount - amount
                self.save()
                recepient.amount += amount
                recepient.save()

                # creating transfer log instance
                transfer_log = transfer_logs(sender=self.account_number,
                                            recepient=recepient.account_number,
                                            amount= amount)

                transfer_log.save()
            else:
                           #for insufficient balance
                raise InsufficientbalanceError("Insufficient Balance")

        else:           #for authentication errors
           raise WrongPinError("PIN supplied is not correct")

    def withdraw(self,amount,pin):
        if self.pin != pin:
            raise WrongPinError("PIN supplied is not correct")

        if self.amount - amount < 0:
            raise InsufficientbalanceError("Insufficient Balance")

        self.amount -= amount
        self.save()

        log = WithdrawalLog(
            account_no= str(self.account_number),
            amount = amount,
        )
        coupon_code = log.save()
        return coupon_code

    def deposit(self,code,depositor_first_name,depositor_last_name):
        try:
            withdraw_log = WithdrawalLog.objects.get(coupon_code=code)
        except Exception:
            raise ValidationError("Code is not valid")
        if withdraw_log.redeemed:
            raise ValidationError("Coupon has already been used")
        
        try:
            if not (DepositLog.objects.filter(code=code).exists()):
                Depo_log = DepositLog(depositor_first_name=depositor_first_name,
                depositor_last_name=depositor_last_name,
                account=self.account_number,
                code=code)
                Depo_log.save()

        except Exception as e:
            print(e,'depositlog exception')

        withdraw_log.redeemed = True
        self.amount += withdraw_log.amount
        self.save()
        withdraw_log.save()