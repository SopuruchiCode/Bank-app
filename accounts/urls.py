from django.urls import path
from . import views


urlpatterns = [
    path("signup/",views.signup,name="signup"),
    path("mylogin/",views.my_login_view,name="mylogin")
]