from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from datetime import datetime


#   User Model Class
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, user_type=None, is_active=True, is_staff=False, is_admin=False, is_verified=False, is_complete=False, steps=None):
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
        user.steps = steps
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, user_type='AD', steps='NA'):
        user = self.create_user(
            email,
            password=password,
            user_type=user_type,
            is_verified=True,
            is_staff=True,
            is_admin=True,
            is_complete=True,
            steps=steps
        )
        return user


class Users(AbstractBaseUser):
    ADMIN = 'AD'
    INDIVIDUAL = 'IN'
    COMPANY = 'CO'
    USER_TYPE = (
        (ADMIN, 'Admin'),
        (INDIVIDUAL, 'Individual'),
        (COMPANY, 'Company'),
    )

    NOTAPPLICABLE = 'NA'
    NOTSTARTED = 'NS'
    COMPLETE = 'CP'
    STEPS = (
        (NOTSTARTED, 'Not Started'),
        (NOTAPPLICABLE, 'Not Applicable'),
        (COMPLETE, 'Complete'),
    )

    email = models.EmailField('email address', unique=True, max_length=255)
    user_type = models.CharField(
        max_length=2, choices=USER_TYPE, null=True, blank=True, default=INDIVIDUAL)
    active = models.BooleanField("Active status", default=True)  # can login
    complete = models.BooleanField(
        "Profile Complete", default=False)  # profile complete
    staff = models.BooleanField(
        "Staff status", default=False)  # staff user non super user
    admin = models.BooleanField("Admin status", default=False)  # super user
    verified = models.BooleanField("Verification status", default=False)
    steps = models.CharField(
        max_length=2, choices=STEPS, blank=True, null=True, default=NOTSTARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # username
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
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_verified(self):
        return self.verified

    @property
    def is_complete(self):
        return self.complete

    class Meta:
        db_table = 'flow_user'
        ordering = ('created_at',)

    def __str__(self):
        return str("{}".format(self.id))
