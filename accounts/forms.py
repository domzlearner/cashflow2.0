# this is not used anymore

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import User

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class CurrencyChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['currency']

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})