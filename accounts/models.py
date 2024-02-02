from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    avatar = models.FileField(upload_to='pics', blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
