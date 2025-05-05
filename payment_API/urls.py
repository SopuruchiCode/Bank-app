from django.urls import path
from .views import key_payment_page, get_current_price,payment_gateway_page,payment_result_page

urlpatterns = [
    path('key-payment/', key_payment_page),
    path('price-per-day-inquiry/', get_current_price),
    path('payment-gateway/', payment_gateway_page),
    path('payment-result/', payment_result_page),
]