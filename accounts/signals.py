from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User 

@receiver(post_save, sender=User)
def user(sender, instance, created, **kwargs):
    if created:
        print(f'user: {instance.email}')