import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a Property is created or updated.
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    logger.info(f"Cache invalidated for key '{cache_key}' after Property save: {instance.title}")


@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a Property is deleted.
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    logger.info(f"Cache invalidated for key '{cache_key}' after Property delete: {instance.title}")
