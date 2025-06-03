from django.urls import path
from .views import PropertySearchView, AutocompleteView

urlpatterns = [
    path('', PropertySearchView.as_view(), name='property-search'),
    path('autocomplete/', AutocompleteView.as_view(), name='autocomplete'),
]