from django.urls import path
from . import views

urlpatterns = [
    path("", views.withdrawal_page),
    path("withdraw-newest-coupon-code-js/", views.newest_coupon_code),
]