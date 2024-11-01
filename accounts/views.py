
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # update once transaction is created
            print(user)
            return redirect('transactions:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # update once transaction is created
                print(user)
                return redirect('transactions:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
@login_required
def settings(request):
    return render(request, 'accounts/settings.html')

@login_required
@require_POST
def update_email(request):
    data = json.loads(request.body)
    new_email = data.get('email')
    if new_email:
        request.user.email = new_email
        request.user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@require_POST
def update_password(request):
    data = json.loads(request.body)
    new_password = data.get('password')
    if new_password:
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@require_POST
def update_currency(request):
    data = json.loads(request.body)
    new_currency = data.get('currency')
    if new_currency in dict(request.user.CURRENCY_CHOICES).keys():
        request.user.currency = new_currency
        request.user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})