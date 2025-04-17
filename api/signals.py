from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from api.models import Product


@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    Invalidate the product cache when a product is saved or deleted.
    """
    cache.delete_pattern("*product_list*")
