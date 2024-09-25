
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'transaction_type', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        sender_profile = data['sender'].clientprofile
        amount = data['amount']

        if data['transaction_type'] in ['withdrawal', 'payment']:
            if sender_profile.balance < amount:
                raise serializers.ValidationError("Insufficient funds for withdrawal or payment.")

        return data
