from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'compte', 'date', 'description', 'amount', 'type', 'created_at', 'updated_at']
