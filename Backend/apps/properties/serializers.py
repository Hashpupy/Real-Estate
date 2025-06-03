from rest_framework import serializers
from .models import (Property, PropertyType, Amenity, PropertyImage, 
                    VirtualTour, FavoriteProperty, PropertyView)
from accounts.serializers import UserSerializer

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class VirtualTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTour
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    property_type = PropertyTypeSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    agent = UserSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = '__all__'
        extra_kwargs = {'location': {'write_only': True}}
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False
    
    def get_view_count(self, obj):
        return obj.views.count()

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ['owner', 'agent', 'status', 'featured', 
                  'created_at', 'updated_at', 'views']

class FavoritePropertySerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    
    class Meta:
        model = FavoriteProperty
        fields = ['id', 'property', 'created_at', 'notes']
    
    def validate(self, data):
        if FavoriteProperty.objects.filter(
            user=self.context['request'].user,
            property=self.context['property']
        ).exists():
            raise serializers.ValidationError("Property already in favorites")
        return data

class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyView
        fields = '__all__'
        read_only_fields = ['user', 'session_key', 'ip_address', 'viewed_at']