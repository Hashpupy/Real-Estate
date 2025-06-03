from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PropertyViewSet, PropertyTypeViewSet, AmenityViewSet,
                   PropertyImageViewSet, VirtualTourViewSet,
                   FavoritePropertyViewSet, NearbyPropertiesView,
                   PropertyStatsView)

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'property-types', PropertyTypeViewSet, basename='propertytype')
router.register(r'amenities', AmenityViewSet, basename='amenity')
router.register(r'property-images', PropertyImageViewSet, basename='propertyimage')
router.register(r'virtual-tours', VirtualTourViewSet, basename='virtualtour')
router.register(r'favorites', FavoritePropertyViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('properties/nearby/', NearbyPropertiesView.as_view(), name='nearby-properties'),
    path('properties/<int:pk>/stats/', PropertyStatsView.as_view(), name='property-stats'),
]