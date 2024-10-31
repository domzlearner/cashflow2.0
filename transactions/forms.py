
from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'category', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.transaction_type = kwargs.pop('transaction_type', 'expense')
        super().__init__(*args, **kwargs)
        
        if self.transaction_type == 'income':
            del self.fields['category']
        else:
            self.fields['category'].widget = forms.Select(choices=Transaction.EXPENSE_CATEGORIES)
            self.fields['category'].required = True

    def clean(self):
        cleaned_data = super().clean()
        if self.transaction_type == 'expense' and not cleaned_data.get('category'):
            raise forms.ValidationError("Category is required for expenses.")
        return cleaned_data