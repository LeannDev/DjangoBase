from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User
from .models import ProfileModel


# Profile auto created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        ProfileModel.objects.create(user=instance)
        user = User.objects.get(pk=instance.pk)
        
        if not user.is_superuser:
            user.is_active = False
            user.save()