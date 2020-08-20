from django import forms

class verificationForm(forms.Form):
    verificationnumber = forms.CharField(max_length=6)
