from rest_framework import serializers
from .models import Transaction, SubscriptionPlan, UserSubscription
from properties.serializers import PropertySerializer
from accounts.serializers import UserSerializer

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserSubscription
        fields = '__all__'
        read_only_fields = ['user', 'start_date', 'end_date', 'is_active']

class TransactionSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    recipient_agent = UserSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['status', 'created_at', 'updated_at']

class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'payment_method', 'property', 'transaction_type']
    
    def validate(self, data):
        # Add validation logic based on transaction type
        return data

class PaymentIntentSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    currency = serializers.CharField(default='usd')
    payment_method_types = serializers.ListField(
        child=serializers.CharField(),
        default=['card']
    )
    description = serializers.CharField(required=False)