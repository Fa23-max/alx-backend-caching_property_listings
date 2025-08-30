import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Get all properties with low-level caching.
    Checks Redis cache first, fetches from database if not found,
    and stores in cache for 1 hour.
    """
    cache_key = 'all_properties'
    
    # Try to get from cache first
    properties = cache.get(cache_key)
    
    if properties is None:
        # Cache miss - fetch from database
        logger.info("Cache miss for all_properties - fetching from database")
        properties = list(Property.objects.all())
        
        # Store in cache for 1 hour (3600 seconds)
        cache.set(cache_key, properties, 3600)
        logger.info(f"Cached {len(properties)} properties for 1 hour")
    else:
        logger.info(f"Cache hit for all_properties - returning {len(properties)} properties")
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with cache statistics.
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis info
        info = redis_conn.info()
        
        # Extract keyspace statistics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) * 100 if total_requests > 0 else 0
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2),
            'used_memory': info.get('used_memory_human', 'N/A'),
            'connected_clients': info.get('connected_clients', 0),
        }
        
        # Log metrics
        logger.info(f"Redis Cache Metrics: {metrics}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0,
        }
