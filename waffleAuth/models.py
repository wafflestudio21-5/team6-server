from django.contrib.auth.models import AbstractUser
from django.db import models

def profile_photo_path(instance, filename):
    # Create a custom file path
    # For example, using the user's ID and original filename
    return f'profile_photos/user_{instance.id}/{filename}'

def background_photo_path(instance, filename):
    # Create another custom file path
    # For example, using the user's ID and original filename
    return f'background_photos/user_{instance.id}/{filename}'


class WaffleUser(AbstractUser):
    nickname = models.CharField(max_length=20, null=False, blank=True)
    email = models.EmailField(null=True, blank=True)
    bio = models.CharField(max_length=60, blank=True)
    profile_photo = models.FileField(upload_to=profile_photo_path, null=True, blank=True)
    background_photo = models.FileField(upload_to=background_photo_path, null=True, blank=True)
    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False
    )

    def __str__(self):
        if self.nickname:
            return self.nickname
        return self.username

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = f'{self.username}{self.pk}'
        super(WaffleUser, self).save(*args, **kwargs)  # Call the "real" save() method.

        if self.nickname == f'{self.username}None':
            # Update the nickname now that self.pk is not None
            self.nickname = f'{self.username}{self.pk}'
            super(WaffleUser, self).save(update_fields=['nickname'])
        
        if not self.following.exists():
            admin_user = WaffleUser.objects.get(username='admin')
            self.following.add(admin_user)
            super(WaffleUser, self).save(*args, **kwargs)
