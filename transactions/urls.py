
from django.urls import path
from . import views
from .views import UpdateTransaction, DeleteTransaction

app_name = 'transactions'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('update/<int:pk>/', UpdateTransaction.as_view(), name='update_transaction'),
    path('delete/<int:pk>/', DeleteTransaction.as_view(), name='delete_transaction'),
]