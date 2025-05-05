from django import forms
from .models import generate_unique_id,Account
from accounts.models import CustomUser

class AccountCreationForm(forms.ModelForm):
    def __init__(self,user, *args, **kwargs):
        super(AccountCreationForm,self).__init__(*args, **kwargs)
        self.fields["client"].initial = user
        self.fields["client"].empty_label = None
        self.fields["client"].queryset = CustomUser.objects.filter(bvn=user.bvn)
        

    pin = forms.CharField(max_length=4,min_length=4,widget= forms.PasswordInput(attrs={"class":"pin-input","placeholder":"PIN"}))

    class Meta:

        model = Account
        fields = ["client","pin"]
        widgets = {"client": forms.Select(attrs={"class":"bvn-choice"})}
        

    def save(self,commit=True):
        account = super(AccountCreationForm,self).save(commit=False)
        if commit:
            account.save()
        return account



# self.fields['client'].queryset = user.account_set.all()

# def check_if_digit(value):
#     if not (value.isdigit()):
#         raise forms.ValidationError("PIN can only exist as a 4 digit code")


# class new_client_form(forms.Form):
#     first_name = forms.CharField(max_length=200, 
#                                  min_length=3,
#                                  widget = forms.TextInput(attrs={"class": "first-name",
#                                                                  "placeholder": "First Name"}))

#     last_name = forms.CharField(max_length=200,
#                                 min_length=3,
#                                 widget = forms.TextInput(attrs={"class": "last-name",
#                                                                 "placeholder": "Last Name"}))

#     pin = forms.CharField(min_length=4,
#                           max_length=4,
#                           validators=[check_if_digit],
#                           widget = forms.PasswordInput(attrs={"class": "pin",
#                                                           "placeholder": "PIN"}))

#     confirmed_pin = forms.CharField(min_length=4,
#                                     max_length=4,
#                                     validators=[check_if_digit],
#                                     widget = forms.PasswordInput(attrs={"class":"con-pin",
#                                                                     "placeholder": "Confirmed PIN"}))
#     password = forms.CharField(min_length=1,
#                                     max_length=40,
#                                     widget = forms.PasswordInput(attrs={"class":"password",
#                                                                     "placeholder": "Password"}))
#     confirmed_password = forms.CharField(min_length=1,
#                                     max_length=40,
#                                     widget = forms.PasswordInput(attrs={"class":"con-password",
#                                                                     "placeholder": "Confirmed Password"}))

#     def clean(self):
#         cleaned_data = super().clean()
#         pin1 = cleaned_data.get("pin")
#         pin2 = cleaned_data.get("confirmed_pin")

#         if pin1 != pin2:
#             raise forms.ValidationError("Please confirm that the pins given are the same")

#         password1 = cleaned_data.get("password")
#         password2  = cleaned_data.get("confirmed_password")

#         if password1 != password2:
#             raise forms.ValidationError("Please confirm that the passwords given are the same")

# class LoginForm(forms.Form):
#     account_no = forms.CharField(max_length=8,min_length=8,
#                                  widget=forms.TextInput(attrs={
#                                      "class":"account-no",
#                                      "placeholder":"Account No"
#                                  }))
#     password = forms.CharField(max_length=1,min_length=40,
#                           widget=forms.PasswordInput(attrs={
#                               "class":"password",
#                               "placeholder":"Password"
#                           }))
