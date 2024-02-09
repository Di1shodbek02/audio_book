import secrets
from http.client import HTTPException

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .models import Book, Notification, UserPersonalize, Audio, File

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


@receiver(post_save, sender=Audio)
def update_hashcode_for_audio(sender, instance, created, **kwargs):
    if created:
        try:
            audio = Audio.objects.select_for_update().get(pk=instance.id)
            hashcode = secrets.token_hex(32)
            audio.hashcode = hashcode
            audio.save()

        except Exception as e:
            raise HTTPException(status_code=400, detail=e)
        return {'success': True, 'message': 'Hashcode Created Successfully'}


@receiver(post_save, sender=File)
def update_hashcode_for_audio(sender, instance, created, **kwargs):
    if created:
        try:
            file = File.objects.select_for_update().get(pk=instance.id)
            hashcode = secrets.token_hex(32)
            file.hashcode = hashcode
            file.save()

        except Exception as e:
            raise HTTPException(status_code=400, detail=e)
        return {'success': True, 'message': 'Hashcode Created Successfully'}
