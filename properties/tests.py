from django.test import TestCase
from django.core.cache import cache
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics


class PropertyModelTest(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            title="Test Property",
            description="A test property description",
            price=100000.00,
            location="Test City"
        )

    def test_property_creation(self):
        self.assertEqual(self.property.title, "Test Property")
        self.assertEqual(self.property.price, 100000.00)
        self.assertEqual(self.property.location, "Test City")

    def test_property_str_method(self):
        self.assertEqual(str(self.property), "Test Property")


class CachingTest(TestCase):
    def setUp(self):
        # Clear cache before each test
        cache.clear()
        
        # Create test properties
        Property.objects.create(
            title="Property 1",
            description="Description 1",
            price=100000.00,
            location="City 1"
        )
        Property.objects.create(
            title="Property 2",
            description="Description 2",
            price=200000.00,
            location="City 2"
        )

    def test_get_all_properties_caching(self):
        # First call should cache the results
        properties1 = get_all_properties()
        self.assertEqual(len(properties1), 2)
        
        # Second call should return cached results
        properties2 = get_all_properties()
        self.assertEqual(len(properties2), 2)
        
        # Verify cache is being used
        cached_properties = cache.get('all_properties')
        self.assertIsNotNone(cached_properties)
        self.assertEqual(len(cached_properties), 2)

    def test_cache_invalidation_on_save(self):
        # Cache the properties
        get_all_properties()
        self.assertIsNotNone(cache.get('all_properties'))
        
        # Create a new property (should invalidate cache)
        Property.objects.create(
            title="New Property",
            description="New Description",
            price=150000.00,
            location="New City"
        )
        
        # Cache should be invalidated
        self.assertIsNone(cache.get('all_properties'))

    def test_cache_invalidation_on_delete(self):
        # Cache the properties
        get_all_properties()
        self.assertIsNotNone(cache.get('all_properties'))
        
        # Delete a property (should invalidate cache)
        property_to_delete = Property.objects.first()
        property_to_delete.delete()
        
        # Cache should be invalidated
        self.assertIsNone(cache.get('all_properties'))
