from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from stores.models import Product, Store

@receiver(post_save, sender=Product)
def product(sender, instance, created, **kwargs):
    if created:
        print(f'product: {instance.name} in {instance.store.name}')
        
@receiver(post_delete, sender=Store)
def deleted(sender, instance, **kwargs):
    print(f'deleted: {instance.name} of {instance.owner}')