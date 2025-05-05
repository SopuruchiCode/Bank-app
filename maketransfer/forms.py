from django import forms
from accounts.models import CustomUser
from openaccount.models import Account

class TransferForm(forms.Form):
    def __init__(self,user,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["acc_of_sender"] = forms.ModelChoiceField(queryset=Account.objects.filter(client=user),empty_label="Select account")
        self.fields["acc_of_sender"].widget.attrs["class"] = "acc-of-sender"
        self.fields["amount"] = forms.FloatField(min_value=100.00,widget=forms.NumberInput(attrs={"class":"trans-amount-input","placeholder":"Amount"}))
        self.fields["rec_account"] = forms.CharField(min_length=8,max_length=8,widget=forms.TextInput(attrs={"class":"rec-account","placeholder":"Recepient Account"}))
        self.fields["pin"] = forms.CharField(max_length=4,widget=forms.PasswordInput(attrs={"class":"pin-input","placeholder":"PIN"}))
       

    def clean(self):
        data = super().clean()
        acc_pin = data.get("pin")
        account = data.get("acc_of_sender")

        if account.pin != acc_pin:
            raise forms.ValidationError("PIN supplied is not correct.")


    