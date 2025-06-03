from django.db import models
from accounts.models import User
from properties.models import Property

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    TYPE_CHOICES = (
        ('deposit', 'Deposit'),
        ('full_payment', 'Full Payment'),
        ('commission', 'Commission'),
        ('subscription', 'Subscription'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50)
    payment_reference = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For commission payments
    recipient_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='commissions')
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} ({self.status})"

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    max_listings = models.PositiveIntegerField()
    featured_listings = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"