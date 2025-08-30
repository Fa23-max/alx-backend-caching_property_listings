from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to return all properties with page-level caching.
    """
    properties = get_all_properties()
    
    # Convert queryset to list of dictionaries for JSON response
    properties_data = []
    for property in properties:
        properties_data.append({
            'id': property.id,
            'title': property.title,
            'description': property.description,
            'price': str(property.price),
            'location': property.location,
            'created_at': property.created_at.isoformat(),
        })
    
    return JsonResponse({
        'properties': properties_data,
        'count': len(properties_data)
    })
