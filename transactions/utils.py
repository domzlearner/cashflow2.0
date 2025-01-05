from datetime import datetime, timedelta
from .models import Transaction, Budget
from django.db.models import Sum

def get_month_choices():
    current_date = datetime.now()
    months = []
    for i in range(-12, 12):  # Adjust range as needed
        month_date = current_date + timedelta(days=i * 30)
        value = month_date.strftime("%Y-%m")
        label = month_date.strftime("%B %Y")
        months.append((value, label))
    return months

def get_month_data(user, year, month):
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    transactions = Transaction.objects.filter(
        user=user,
        date__range=(start_date, end_date)
    )
    
    income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    
    expense_categories = list(transactions.filter(type='expense')
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total'))
    
    budgets = Budget.objects.filter(user=user, period=f"{year}-{month:02d}")
    budget_data = {}
    for budget in budgets:
        category_expenses = transactions.filter(type='expense', category=budget.category).aggregate(Sum('amount'))['amount__sum'] or 0
        remaining = budget.amount - category_expenses
        budget_data[budget.category] = {
            'budget': float(budget.amount),
            'consumed': float(category_expenses),
            'remaining': float(remaining)
        }
    
    # Convert all numeric values to float
    return {
        'income': float(income),
        'expenses': float(expenses),
        'expense_categories': [
            {'category': item['category'] or 'Uncategorized', 'total': float(item['total'])}
            for item in expense_categories
        ],
        'budget_data': budget_data
    }