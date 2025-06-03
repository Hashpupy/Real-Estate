from django.contrib import admin
from .models import (Property, PropertyType, Amenity, PropertyImage, 
                    VirtualTour, FavoriteProperty, PropertyView)

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class VirtualTourInline(admin.StackedInline):
    model = VirtualTour
    extra = 0

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'bedrooms', 'bathrooms', 'status')
    list_filter = ('status', 'listing_type', 'property_type', 'city')
    search_fields = ('title', 'address', 'city', 'state')
    inlines = [PropertyImageInline, VirtualTourInline]

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyType)
admin.site.register(Amenity)
admin.site.register(FavoriteProperty)
admin.site.register(PropertyView)