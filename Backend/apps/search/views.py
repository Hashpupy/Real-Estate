from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from haystack.query import SearchQuerySet
from properties.serializers import PropertySerializer

class PropertySearchView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query = request.GET.get('q', '')
        sqs = SearchQuerySet().models(Property).filter(content=query)
        
        # Apply filters from request
        listing_type = request.GET.get('listing_type')
        if listing_type:
            sqs = sqs.filter(listing_type=listing_type)
        
        min_price = request.GET.get('min_price')
        if min_price:
            sqs = sqs.filter(price__gte=min_price)
        
        max_price = request.GET.get('max_price')
        if max_price:
            sqs = sqs.filter(price__lte=max_price)
        
        bedrooms = request.GET.get('bedrooms')
        if bedrooms:
            sqs = sqs.filter(bedrooms=bedrooms)
        
        # Spatial search
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        radius = request.GET.get('radius', 10)  # Default 10km
        
        if lat and lng:
            sqs = sqs.dwithin('location', {'lat': lat, 'lon': lng}, radius)
        
        # Ordering
        ordering = request.GET.get('ordering')
        if ordering:
            if ordering == 'price':
                sqs = sqs.order_by('price')
            elif ordering == '-price':
                sqs = sqs.order_by('-price')
            elif ordering == 'newest':
                sqs = sqs.order_by('-created_at')
        
        # Pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        results = sqs[start:end]
        total = sqs.count()
        
        property_ids = [result.object.id for result in results if result.object]
        properties = Property.objects.filter(id__in=property_ids)
        serializer = PropertySerializer(
            properties, 
            many=True, 
            context={'request': request}
        )
        
        return Response({
            'results': serializer.data,
            'count': total,
            'page': page,
            'page_size': page_size
        })

class AutocompleteView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query = request.GET.get('q', '')
        sqs = SearchQuerySet().models(Property).autocomplete(
            content_auto=query
        )[:5]  # Limit to 5 suggestions
        
        suggestions = []
        for result in sqs:
            suggestions.append({
                'title': result.title,
                'city': result.city,
                'state': result.state,
                'id': result.pk
            })
        
        return Response(suggestions)