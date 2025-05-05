from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=200, 
                                 min_length=3,
                                 widget = forms.TextInput(attrs={"class": "first-name",
                                                                 "placeholder": "First Name"}))

    last_name = forms.CharField(max_length=200,
                                min_length=3,
                                widget = forms.TextInput(attrs={"class": "last-name",
                                                                "placeholder": "Last Name"}))

    password1 = forms.CharField(max_length=200,
                                min_length=3,
                                widget = forms.PasswordInput(attrs={"class": "pass1",
                                                                "placeholder": "Password"}))

    password2 = forms.CharField(max_length=200,
                                min_length=3,
                                widget = forms.PasswordInput(attrs={"class": "pass2",
                                                                "placeholder": "Password"}))


    class Meta:
        model = CustomUser
        fields = ( "first_name",
                    "last_name",
                    "password1",
                    "password2",
        )
    def save(self,commit=True):
        user = super(CustomUserCreationForm,self).save(commit=False)
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
                    "first_name",
                    "last_name",
        )


class my_login_form(forms.Form):
    bvn = forms.CharField(max_length=8,min_length=8,widget=forms.TextInput(attrs={"class":"bvn","placeholder":"Bvn"}))
    password = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"class":"password","placeholder":"Password"}))




# class MyUserCreationForm(forms.Form):
#     first_name = forms.CharField(max_length=200, 
#                                  min_length=3,
#                                  widget = forms.TextInput(attrs={"class": "first-name",
#                                                                  "placeholder": "First Name"}))

#     last_name = forms.CharField(max_length=200,
#                                 min_length=3,
#                                 widget = forms.TextInput(attrs={"class": "last-name",
#                                                                 "placeholder": "Last Name"}))

#     password1 = forms.CharField(max_length=200,
#                                 min_length=3,
#                                 widget = forms.PasswordInput(attrs={"class": "pass1",
#                                                                 "placeholder": "Password"}))

#     password2 = forms.CharField(max_length=200,
#                                 min_length=3,
#                                 widget = forms.PasswordInput(attrs={"class": "pass2",
#                                                                 "placeholder": "Password"}))

    # def clean(self):
    #     data = super().clean()
    #     password1 = data.get("password1")
    #     password2 = data.get("password2")

    #     if password1 != password2:
    #         raise forms.ValidationError("Please confirm passwords")

