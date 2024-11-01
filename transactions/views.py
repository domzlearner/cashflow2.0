
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions/dashboard.html', {'transactions': transactions})

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
    return render(request, 'transactions/transaction_form.html', context)
