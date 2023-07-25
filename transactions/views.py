from dateutil.relativedelta import relativedelta
from django.shortcuts import render,redirect
from .models import Customer
# from django.contrib.auth.models import User
# from transactions.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView

from transactions.constants import DEPOSIT, WITHDRAWAL

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from accounts.models import UserBankAccount, BankAccountType
from decimal import Decimal

# def Transaction_Result(request, result):
#     return render(request, 'transactions/transaction_res.html', {'result': result})


from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm,
)
from transactions.models import Transaction


class TransactionRepostView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def get(self, request, *args, **kwargs):
        form = TransactionDateRangeForm(request.GET or None)
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )

        daterange = self.form_data.get("daterange")

        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account,
            'form': TransactionDateRangeForm(self.request.GET or None)
        })

        return context


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit Money to Your Account'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        if not account.initial_deposit_date:
            now = timezone.now()
            next_interest_month = int(
                12 / account.account_type.interest_calculation_per_year
            )
            account.initial_deposit_date = now
            account.interest_start_date = (
                now + relativedelta(
                    months=+next_interest_month
                )
            )

        account.balance += amount
        account.save(
            update_fields=[
                'initial_deposit_date',
                'balance',
                'interest_start_date'
            ]
        )

        messages.success(
            self.request,
            f'₹{amount} was deposited to your account successfully'
        )

        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money from Your Account'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.account.balance -= form.cleaned_data.get('amount')
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn ₹ {amount} from your account'
        )

        return super().form_valid(form)

#@login_required
def transfer_money(request):
    if request.method == 'POST':
        sender_account = request.user.account
        receiver_account_no = request.POST.get('receiver_account_no')
        amount = float(request.POST.get('amount'))

        # Check if sender and receiver are different
        if sender_account.account_no == receiver_account_no:
            messages.error(request, 'You cannot transfer to your own account.')
        else:
            try:
                receiver_account = UserBankAccount.objects.get(account_no=receiver_account_no)
            except UserBankAccount.DoesNotExist:
                messages.error(request, 'Receiver account not found.')
            else:
                if sender_account.balance >= amount:
                    sender_account.balance -= Decimal(amount)
                    receiver_account.balance += Decimal(amount)
                    sender_account.save()
                    receiver_account.save()

                    # Create a new transaction object
                    transaction = Transaction.objects.create(
                        account=sender_account,
                        transaction_type=Transaction.TRANSFER,
                        amount=Decimal(amount),
                        timestamp=timezone.now(),
                        balance_after_transaction=sender_account.balance,
                    )
                    transaction.save()

                    messages.success(request, 'Transaction successful.')
                    return redirect('transactions:transaction_report')
                else:
                    messages.error(request, 'Insufficient balance.')
                    # Render the same transfer_money page with form data
                    user_bank_accounts = UserBankAccount.objects.exclude(user=request.user)
                    account_types = BankAccountType.objects.all()
                    params = {'user_bank_accounts': user_bank_accounts, 'account_types': account_types, 'form_data': request.POST}
                    return render(request, "transactions/transfer_money.html", params)

    # GET request or form data with errors
    user_bank_accounts = UserBankAccount.objects.exclude(user=request.user)
    account_types = BankAccountType.objects.all()
    params = {'user_bank_accounts': user_bank_accounts, 'account_types': account_types, 'form_data': request.POST}
    return render(request, "transactions/transfer_money.html", params)


# @login_required
# def transfer_money(request):
#     if request.method == 'POST':
#         sender_account = request.user.account
#         receiver_account_no = request.POST.get('receiver_account_no')
#         amount = float(request.POST.get('amount'))

#         # Check if sender and receiver are different
#         if sender_account.account_no == receiver_account_no:
#             messages.error(request, 'You cannot transfer to your own account.')
#         else:
#             try:
#                 receiver_account = UserBankAccount.objects.get(account_no=receiver_account_no)
#             except UserBankAccount.DoesNotExist:
#                 messages.error(request, 'Receiver account not found.')
#             else:
#                 if sender_account.balance >= amount:
#                    sender_account.balance -= Decimal(amount)
#                    receiver_account.balance += Decimal(amount)
#                    sender_account.save()
#                    receiver_account.save()

#                    # Create a new transaction object
#                    transaction = Transaction.objects.create(
#                        account=sender_account,
#                        transaction_type=Transaction.TRANSFER,
#                        amount=Decimal(amount),
#                        timestamp=timezone.now(),
#                        balance_after_transaction=sender_account.balance,
#                    )
#                    transaction.save()

#                    messages.success(request, 'Transaction successful.')
#                    return redirect('transactions:transaction_report')
                   
#                 else:
#                     messages.error(request, 'Insufficient balance.')

#     # Get list of all user bank accounts except for the sender
#     user_bank_accounts = UserBankAccount.objects.exclude(user=request.user)
#     account_types = BankAccountType.objects.all()
#     params = {'user_bank_accounts': user_bank_accounts, 'account_types': account_types}
#     return render(request, "transactions/transfer_money.html", params)
