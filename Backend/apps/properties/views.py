from rest_framework import viewsets, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunc
from .models import (Property, PropertyType, Amenity, PropertyImage, 
                    VirtualTour, FavoriteProperty, PropertyView)
from .serializers import (PropertySerializer, PropertyTypeSerializer, 
                         AmenitySerializer, PropertyImageSerializer, 
                         VirtualTourSerializer, PropertyCreateSerializer,
                         FavoritePropertySerializer, PropertyViewSerializer)
from .filters import PropertyFilter
from utils.permissions import IsOwnerOrAgent, IsAgentOrReadOnly
from utils.pagination import StandardResultsSetPagination

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'city', 'state', 'zip_code', 'address']
    ordering_fields = ['price', 'bedrooms', 'square_footage', 'created_at']
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PropertyCreateSerializer
        return PropertySerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated, IsAgentOrReadOnly]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrAgent]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        if self.request.user.user_type == 'agent':
            serializer.save(owner=self.request.user, agent=self.request.user)
        else:
            serializer.save(owner=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        PropertyView.objects.create(
            property=instance,
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key if request.session else None,
            ip_address=self.get_client_ip(request)
        )
        return super().retrieve(request, *args, **kwargs)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class NearbyPropertiesView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        latitude = self.request.query_params.get('lat')
        longitude = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 10)  # Default 10km

        if not latitude or not longitude:
            return Property.objects.none()

        user_location = Point(float(longitude), float(latitude), srid=4326)
        return Property.objects.filter(
            location__distance_lte=(user_location, Distance(km=radius))
        ).annotate(
            distance=DistanceFunc('location', user_location)
        ).order_by('distance')

class PropertyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    permission_classes = [permissions.AllowAny]

class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAgent]
    
    def get_queryset(self):
        return self.queryset.filter(property__owner=self.request.user)

class VirtualTourViewSet(viewsets.ModelViewSet):
    queryset = VirtualTour.objects.all()
    serializer_class = VirtualTourSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAgent]

class FavoritePropertyViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritePropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FavoriteProperty.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        property_id = self.request.data.get('property')
        serializer.save(user=self.request.user, property_id=property_id)

class PropertyStatsView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAgent]
    
    def retrieve(self, request, *args, **kwargs):
        property = self.get_object()
        views = property.views.count()
        favorites = property.favorites.count()
        
        return Response({
            'views': views,
            'favorites': favorites,
            'views_by_day': self.get_views_by_day(property),
            'views_by_month': self.get_views_by_month(property),
        })
    
    def get_views_by_day(self, property):
        # Implement view aggregation by day
        pass
    
    def get_views_by_month(self, property):
        # Implement view aggregation by month
        pass