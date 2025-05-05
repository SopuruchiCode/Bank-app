from django.contrib import admin
from .models import EpaymentSubscription,Transaction_detail,PaymentLogging

# Register your models here.
admin.site.register(EpaymentSubscription)
admin.site.register(Transaction_detail)
admin.site.register(PaymentLogging)
