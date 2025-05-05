from django.urls import path
from . import views

urlpatterns = [
    path("",views.homepage,name='welcome'),
    path("create-account/",views.open_account,name='accountform'),
    path("acc-info/",views.account_info_view),
]