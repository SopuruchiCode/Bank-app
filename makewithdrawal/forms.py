from openaccount.models import Account
from django import forms

class WithdrawalForm(forms.Form):
    def __init__(self,user,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["account_no"] = forms.ModelChoiceField(queryset=Account.objects.filter(client=user),empty_label='Select Account')
        self.fields["amount"] = forms.FloatField(min_value=100,widget=forms.NumberInput(attrs={"placeholder":"Amount"}))
        self.fields['pin'] = forms.CharField(max_length=10,widget=forms.PasswordInput(attrs={"placeholder":"PIN"}))

    def clean(self):
        data = super().clean()
        account = data.get("account_no")
        pin = data.get("pin")
        amount = data.get("amount")

        if account.pin != pin:
            raise forms.ValidationError("PIN is not correct")
