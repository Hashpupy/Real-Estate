import django_filters
from .models import Property
from django.db.models import Q

class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    bedrooms = django_filters.NumberFilter(field_name='bedrooms')
    min_bathrooms = django_filters.NumberFilter(field_name='bathrooms', lookup_expr='gte')
    min_sqft = django_filters.NumberFilter(field_name='square_footage', lookup_expr='gte')
    property_type = django_filters.CharFilter(field_name='property_type__name')
    listing_type = django_filters.CharFilter(field_name='listing_type')
    amenities = django_filters.CharFilter(method='filter_amenities')
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Property
        fields = []
    
    def filter_amenities(self, queryset, name, value):
        amenity_ids = value.split(',')
        return queryset.filter(amenities__id__in=amenity_ids).distinct()
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(city__icontains=value) |
            Q(state__icontains=value) |
            Q(zip_code__icontains=value) |
            Q(address__icontains=value)
        )