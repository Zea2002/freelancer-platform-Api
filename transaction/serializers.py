
from rest_framework import serializers
from .models import Transaction
from user.models import ClientProfile  

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, data):
        if data['transaction_type'] in ['withdrawal', 'payment']:
            sender_profile = ClientProfile.objects.get(user=data['sender']) 
            if sender_profile.balance < data['amount']:
                raise serializers.ValidationError('Insufficient funds.')
        return data
