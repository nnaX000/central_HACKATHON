from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    user_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    def __str__(self):
        return self.username
