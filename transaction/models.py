
from django.db import models
from user.models import User
from user.models import ClientProfile,FreelancerProfile 

TRANSACTION_TYPES = (
    ('deposit', 'Deposit'),
    ('withdrawal', 'Withdrawal'),
    ('payment', 'Payment'),
)

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction from {self.sender.username} to {self.receiver.username} of ${self.amount}'

    def save(self, *args, **kwargs):
        sender_profile = ClientProfile.objects.get(user=self.sender)  # Adjust to your profile model
        receiver_profile = FreelancerProfile.objects.get(user=self.receiver)  # Adjust to your profile model

        if self.transaction_type == 'deposit':
            receiver_profile.balance += self.amount
        elif self.transaction_type == 'withdrawal':
            sender_profile.balance -= self.amount
        elif self.transaction_type == 'payment':
            sender_profile.balance -= self.amount
            receiver_profile.balance += self.amount

        if sender_profile.balance < 0:
            raise ValueError('Insufficient funds for withdrawal or payment.')

        # Save profiles first to update balances
        receiver_profile.save()
        sender_profile.save()

        # Now save the transaction
        super().save(*args, **kwargs)
