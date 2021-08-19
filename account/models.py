from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, mail, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        return self.create_user(mail, name, password, **other_fields)
    def create_user(self, mail, name, password, **other_fields):
        mail = self.normalize_email(mail)
        user = self.model(mail=mail, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class UserBase(AbstractBaseUser, PermissionsMixin):
    mail = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'),max_length=150)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_sender = models.BooleanField(default=False)
    is_shipe = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS=['name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.mail

