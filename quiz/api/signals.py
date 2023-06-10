from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Friendship


@receiver(post_save, sender=User)
def create_friendship(sender, instance, created, **kwargs):
    if created:
        Friendship.objects.create(from_user=instance,to_user=1)
        Friendship.objects.create(from_user=1,to_user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    fr1=Friendship.objects.get(from_user=instance)
    fr2=Friendship.objects.get(to_user=instance)
    fr1.save()
    fr2.save()