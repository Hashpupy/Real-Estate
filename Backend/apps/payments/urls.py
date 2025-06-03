from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (TransactionViewSet, SubscriptionPlanViewSet,
                   UserSubscriptionViewSet, CreatePaymentIntentView,
                   WebhookView)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscriptionplan')
router.register(r'user-subscriptions', UserSubscriptionViewSet, basename='usersubscription')

urlpatterns = [
    path('', include(router.urls)),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('webhook/', WebhookView.as_view(), name='stripe-webhook'),
]