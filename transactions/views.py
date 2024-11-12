
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm
from django.db.models import Sum
from datetime import datetime, timedelta
from django.db.models import Max
from django.http import JsonResponse
from django.utils.decorators import method_decorator
import json

def get_month_choices():
    end_date = datetime.now().date().replace(day=1)
    start_date = end_date - timedelta(days=365)
    months = []
    current = start_date
    while current <= end_date:
        months.append((current.strftime('%Y-%m'), current.strftime('%B %Y')))
        current += timedelta(days=32)
        current = current.replace(day=1)
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
    
    # Convert all numeric values to float
    return {
        'income': float(income),
        'expenses': float(expenses),
        'expense_categories': [
            {'category': item['category'] or 'Uncategorized', 'total': float(item['total'])}
            for item in expense_categories
        ]
    }

@login_required
def dashboard(request):
    selected_month = request.GET.get('month', datetime.now().strftime('%Y-%m'))
    year, month = map(int, selected_month.split('-'))
    
    month_data = get_month_data(request.user, year, month)
    
    # Income vs Expense breakdown
    income_vs_expense = [
        {'name': 'Income', 'value': float(month_data['income'])},
        {'name': 'Expenses', 'value': float(month_data['expenses'])},
    ]

    transactions = Transaction.objects.filter(user=request.user).annotate(latest_date=Max('date')).order_by('-date')[:10]
    
    context = {
        'transactions': transactions,
        'month_choices': get_month_choices(),
        'selected_month': selected_month,
        'income': float(month_data['income']),
        'expenses': float(month_data['expenses']),
        'balance': float(month_data['income'] - month_data['expenses']),
        'income_vs_expense': json.dumps(income_vs_expense),
        'expense_categories': json.dumps(month_data['expense_categories']),
    }
    
    # print("Income vs Expense Data:", income_vs_expense)
    # print("Expense Categories Data:", month_data['expense_categories'])
    print("balance:", float(month_data['income'] - month_data['expenses']))
    
    return render(request, 'transactions/dashboard.html', context)

@login_required
def add_transaction(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    transaction_type = request.GET.get('type', 'expense')
    if request.method == 'POST':
        form = TransactionForm(request.POST, transaction_type=transaction_type)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.type = transaction_type
            transaction.save()
            return redirect('transactions:dashboard')
    else:
        form = TransactionForm(transaction_type=transaction_type)
    
    context = {
        'form': form,
        'transaction_type': transaction_type,
        'transactions': transactions
    }
    return render(request, 'transactions/add_transaction_form.html', context)

@method_decorator(login_required, name='dispatch')
class UpdateTransaction(View):
    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
        form = TransactionForm(instance=transaction)

        context = {
        'form': form,
        'transaction': transaction,
        'transactions': transactions
        }

        return render(request, 'transactions/update_transaction_form.html', context)

    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            # return JsonResponse({'success': True, 'message': 'Transaction updated successfully!'})
            return JsonResponse({
                'success': True, 
                'message': 'Transaction updated successfully!',
                'redirect_url': reverse('transactions:dashboard')
            })
        return JsonResponse({'success': False, 'message': 'Form is invalid.', 'errors': form.errors}, status=400)

@method_decorator(login_required, name='dispatch')
class DeleteTransaction(View):
    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        transaction.delete()
        return JsonResponse({'success': True, 'message': 'Transaction deleted successfully!'})