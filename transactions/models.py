from django.db import models
from .constants import TRANSACTION_TYPE_CHOICES
from accounts.models import UserBankAccount


class Transaction(models.Model):
    DEPOSIT = 1
    WITHDRAWAL = 2
    TRANSFER = 3
    TRANSACTION_TYPE_CHOICES = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer'),
    )

    # rest of the model code


    account = models.ForeignKey(
        UserBankAccount,
        related_name='transactions',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.account.account_no)

    class Meta:
        ordering = ['timestamp']

# class Transaction(models.Model):
    
#     account = models.ForeignKey(
#         UserBankAccount,
#         related_name='transactions',
#         on_delete=models.CASCADE,
#     )
#     amount = models.DecimalField(
#         decimal_places=2,
#         max_digits=12
#     )
#     balance_after_transaction = models.DecimalField(
#         decimal_places=2,
#         max_digits=12
#     )
#     transaction_type = models.PositiveSmallIntegerField(
#         choices=TRANSACTION_TYPE_CHOICES
#     )
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.account.account_no)

#     class Meta:
#         ordering = ['timestamp']

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    account_number = models.IntegerField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class User(models.Model):
    eno=models.IntegerField()
    ename=models.CharField(max_length=30)
    ebal=models.FloatField()
    
    def __str__(self):
        return 'Customer Object with eno: ' +str(self.eno) 

