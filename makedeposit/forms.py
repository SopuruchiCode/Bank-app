from django import forms

from openaccount.models import Account,WithdrawalLog,DepositLog


class DepositForm(forms.ModelForm):
    code = forms.CharField(max_length=500, widget=forms.TextInput(attrs={"class":"deposit-coupon", "placeholder":"Money Coupon"}))
    class Meta:
        model = DepositLog
        fields = ["depositor_first_name","depositor_last_name","account","code"]
        widgets = {
            "depositor_first_name":forms.TextInput(attrs={"class":"deposit-depositor", "placeholder":"Depositor First Name"}),
            "depositor_last_name":forms.TextInput(attrs={"class":"deposit-depositor", "placeholder":"Depositor Last Name"}),
            "account":forms.TextInput(attrs = {"class":"deposit-account", "placeholder":"Account Number"}),
        }

    def clean_depositor_first_name(self):
        dfn = self.cleaned_data.get("depositor_first_name")
        depositor_first_name = "".join(dfn.split())
        if len(depositor_first_name) < 3:
            raise forms.ValidationError("First Name is too short.")
        return depositor_first_name

    def clean_depositor_last_name(self):
        dln = self.cleaned_data.get("depositor_last_name")
        depositor_last_name = "".join(dln.split())
        if len(depositor_last_name) < 3:
            raise forms.ValidationError("Last Name is too short.")
        return depositor_last_name

    def clean_account(self):
        account = self.cleaned_data.get("account")
        try:
            Account.objects.get(account_number=account)
        except Exception:
            raise forms.ValidationError("Account is not valid")
        return account

    def clean_code(self):
        code = self.cleaned_data.get("code")
        try:
            code_log = WithdrawalLog.objects.get(coupon_code=code)
        except Exception:
            raise forms.ValidationError("Invalid Coupon Code")
        if code_log.redeemed:
            raise forms.ValidationError("Coupon has already been used")
        return code