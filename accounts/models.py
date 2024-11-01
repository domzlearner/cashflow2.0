
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('PHP', 'Philippine Peso'),
        ('JPY', 'Japanese Yen'),
        ('NONE', 'No Currency'),
    ]
    currency = models.CharField(max_length=4, choices=CURRENCY_CHOICES, default='NONE')

    def __str__(self):
        return self.username