# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Add any additional fields you want
    bio = models.TextField(max_length=500, blank=True)
