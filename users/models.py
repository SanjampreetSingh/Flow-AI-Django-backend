from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from datetime import datetime
import random
import string

#   User Model Class


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, user_type=None, is_active=True, is_staff=False, is_admin=False, is_verified=False, is_complete=False):
        if not email:
            raise ValueError("User must have an Email")
        if not password:
            raise ValueError("User must have a Password")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.user_type = user_type
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.verified = is_verified
        user.complete = is_complete
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, user_type='IN'):
        user = self._create_user(
            email,
            password=''.join(random.choices(
                string.ascii_letters + string.digits, k=16)),
            user_type=user_type,
            is_verified=False,
            is_complete=False,
        )
        return user

    def create_superuser(self, email, password=None, user_type='AD'):
        user = self._create_user(
            email,
            password=password,
            user_type=user_type,
            is_verified=True,
            is_staff=True,
            is_admin=True,
            is_complete=True,
        )
        return user


class Users(AbstractBaseUser):
    ADMIN = 'AD'
    INDIVIDUAL = 'IN'
    USER_TYPE = (
        (ADMIN, 'Admin'),
        (INDIVIDUAL, 'Individual'),
    )

    email = models.EmailField('Email Address', unique=True, max_length=255)
    user_type = models.CharField(
        max_length=2, choices=USER_TYPE, null=True, blank=True, default=INDIVIDUAL)
    active = models.BooleanField("Active", default=True)  # can login
    complete = models.BooleanField(
        "Profile Complete", default=False)  # profile complete
    staff = models.BooleanField("Staff", default=False)  # staff user
    admin = models.BooleanField("Admin", default=False)  # super user
    verified = models.BooleanField("Verified", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        db_table = 'flow_user'
        ordering = ('created_at',)

    def __str__(self):
        return str("{}".format(self.id))
