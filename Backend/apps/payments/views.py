import stripe
from django.conf import settings
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, SubscriptionPlan, UserSubscription
from .serializers import (TransactionSerializer, SubscriptionPlanSerializer,
                         UserSubscriptionSerializer, CreateTransactionSerializer,
                         PaymentIntentSerializer)
from utils.permissions import IsAgentOrAdmin

stripe.api_key = settings.STRIPE_SECRET_KEY

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateTransactionSerializer
        return TransactionSerializer
    
    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        
        # Process payment with Stripe
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(transaction.amount * 100),  # Convert to cents
                currency='usd',
                payment_method_types=['card'],
                description=f"Payment for {transaction.get_transaction_type_display()}",
                metadata={
                    'transaction_id': transaction.id,
                    'user_id': self.request.user.id
                }
            )
            
            transaction.payment_reference = payment_intent.id
            transaction.save()
            
        except stripe.error.StripeError as e:
            transaction.status = 'failed'
            transaction.save()
            raise serializers.ValidationError(str(e))

class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated]

class UserSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        plan = serializer.validated_data['plan']
        
        # Process payment
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(plan.price * 100),
                currency='usd',
                payment_method_types=['card'],
                description=f"Subscription for {plan.name}",
            )
            
            # In a real app, you'd complete the payment before creating subscription
            subscription = serializer.save(
                user=self.request.user,
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timezone.timedelta(days=plan.duration_days),
                is_active=True
            )
            
        except stripe.error.StripeError as e:
            raise serializers.ValidationError(str(e))

class CreatePaymentIntentView(generics.CreateAPIView):
    serializer_class = PaymentIntentSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=serializer.validated_data['amount'],
                currency=serializer.validated_data['currency'],
                payment_method_types=serializer.validated_data['payment_method_types'],
                description=serializer.validated_data.get('description', ''),
            )
            
            return Response({
                'clientSecret': intent['client_secret'],
                'id': intent['id']
            })
        
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class WebhookView(generics.CreateAPIView):
    permission_classes = []  # No authentication for webhooks
    
    def create(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return Response({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return Response({'error': 'Invalid signature'}, status=400)
        
        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            self.handle_payment_succeeded(payment_intent)
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            self.handle_payment_failed(payment_intent)
        
        return Response({'success': True})
    
    def handle_payment_succeeded(self, payment_intent):
        try:
            transaction = Transaction.objects.get(
                payment_reference=payment_intent['id']
            )
            transaction.status = 'completed'
            transaction.save()
            
            # Additional logic for completed payments
        except Transaction.DoesNotExist:
            pass
    
    def handle_payment_failed(self, payment_intent):
        try:
            transaction = Transaction.objects.get(
                payment_reference=payment_intent['id']
            )
            transaction.status = 'failed'
            transaction.save()
        except Transaction.DoesNotExist:
            pass