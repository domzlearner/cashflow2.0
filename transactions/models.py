
from django.db import models
from django.conf import settings

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    EXPENSE_CATEGORIES = (
        ('bills', 'Bills'),
        ('debts', 'Debts'),
        ('food', 'Food'),
        ('grocery', 'Grocery'),
        ('savings', 'Savings'),
        ('others', 'Others'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=7, choices=EXPENSE_CATEGORIES, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.type} - {self.description}"