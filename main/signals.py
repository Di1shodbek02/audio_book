from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .models import Book, Notification, UserPersonalize
User = get_user_model()


@receiver(post_save, sender=Book)
def create_special_notification(sender, instance, created, **kwargs):
    if created:
        try:

            user_profiles = UserPersonalize.objects.filter(personalize=instance.category_id)

            for user_profile in user_profiles:

                user = user_profile.user_id

                Notification.objects.create(
                    user_id=user,
                    title="Special Notification For You 📩",
                    text=f"A new book in your personalized category '{instance.category_id.name.upper()}' has been added: {instance.name}",
                    status=False
                )
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Error Occurred')
