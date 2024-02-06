from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .models import Book, Notification  # Import your models
User = get_user_model()


@receiver(post_save, sender=Book)
def create_special_notification(sender, instance, created, **kwargs):
    print(instance)
    if created:
        try:
            user_profile = User.objects.get(username=instance.category_id.name)
            if user_profile.username == instance.category_id.name:

                Notification.objects.create(
                    user_id=user_profile,
                    title="Special Notification",
                    text=f"A new book in your personalized category '{instance.category_id.name}' has been added: {instance.name}",
                    status=False
                )
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Error Occured')
