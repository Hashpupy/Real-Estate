from django.contrib import admin
from .models import Transaction, SubscriptionPlan, UserSubscription

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'transaction_type', 'status', 'created_at')
    list_filter = ('status', 'transaction_type')
    search_fields = ('user__username', 'payment_reference')
    readonly_fields = ('created_at', 'updated_at')

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'max_listings', 'is_active')
    list_editable = ('is_active',)

class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'plan')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)