# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class WaffleUser(AbstractUser):
    nickname = models.CharField(max_length=20)
    bio = models.CharField(max_length=60)
    profile_photo = models.FileField(upload_to='profile_photos/', null=True, blank=True)
    background_photo = models.FileField(upload_to='background_photos/', null=True, blank=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)