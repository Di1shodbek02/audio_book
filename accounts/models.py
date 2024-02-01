from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    avatar = models.FileField(upload_to='pics', blank=
    True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.role.name
