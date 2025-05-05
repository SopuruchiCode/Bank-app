from django.urls import path
from . import views

urlpatterns = [
    path("",views.transfer,name="transfer"),
    path("acc-info/",views.acc_info)
]