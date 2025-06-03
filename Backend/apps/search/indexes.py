from haystack import indexes
from properties.models import Property

class PropertyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    address = indexes.CharField(model_attr='address')
    city = indexes.CharField(model_attr='city')
    state = indexes.CharField(model_attr='state')
    zip_code = indexes.CharField(model_attr='zip_code')
    property_type = indexes.CharField(model_attr='property_type__name')
    listing_type = indexes.CharField(model_attr='listing_type')
    bedrooms = indexes.IntegerField(model_attr='bedrooms')
    bathrooms = indexes.FloatField(model_attr='bathrooms')
    price = indexes.FloatField(model_attr='price')
    square_footage = indexes.IntegerField(model_attr='square_footage')
    location = indexes.LocationField(model_attr='location')
    amenities = indexes.MultiValueField()
    
    def get_model(self):
        return Property
    
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status='active')
    
    def prepare_amenities(self, obj):
        return [amenity.name for amenity in obj.amenities.all()]
    
    def prepare(self, obj):
        data = super().prepare(obj)
        
        # Boost fields
        data['boost'] = 1.0
        if obj.featured:
            data['boost'] = 2.0
        
        return data