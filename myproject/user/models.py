from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.files.storage import FileSystemStorage


class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, username, email, password=None, **extra_fields):
        if not user_id:
            raise ValueError("The User ID must be set")
        email = self.normalize_email(email)
        user = self.model(
            user_id=user_id, username=username, email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(user_id, username, email, password, **extra_fields)


photo_storage = FileSystemStorage(location="myproject/media", base_url="/media")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=255, unique=True, default="default_user_id")
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    photo = models.ImageField(storage=photo_storage, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self):
        return self.username
