from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()


@receiver(pre_save, sender=UserProfile)
def delete_old_profile_picture(sender, instance, **kwargs):
    if not instance.pk:
        try:
            old_profile = UserProfile.objects.get(pk=instance.pk)
            if old_profile.picture != instance.profile_picture:
                old_profile.delete_old_profile_picture()
        except UserProfile.DoesNotExist:
            pass