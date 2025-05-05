from django.urls import path
from . import views

urlpatterns = [
    path("",views.history_page),
    path("js-account-displayed/",views.history_acc_display),
    path("js-transfer-history/",views.transfer_history),
    path("js-withdrawal-history/",views.withdrawal_history),
    path("js-deposit-history/",views.deposit_logs),
]