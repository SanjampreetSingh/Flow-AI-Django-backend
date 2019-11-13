from django.db import models
from datetime import datetime
from users.models import (Users)


# Profile Model Class
class Profiles(models.Model):

    user = models.OneToOneField(
        Users, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flow_user_profile'
        ordering = ('created_at',)


# Profile Image path setting
def profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_image/user_<id>/<filename>
    somelist = filename.split('.')  # spliting orignal file name into somelist
    extension = (somelist[-1])   # Getting last element of the list
    filename = str(instance.user.id) + '_' + \
        str(datetime.now()) + '.' + extension  # Re-writing file name
    return 'user/profile_image/user_{0}/{1}'.format(instance.user.id, filename)


# Avatar Model Class
class ProfilePicture(models.Model):
    user = models.OneToOneField(
        Users, on_delete=models.CASCADE, blank=True, null=True)
    profile_image = models.ImageField(
        "Profile Image", "profile_image", upload_to=profile_directory_path,
        max_length=2083, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flow_user_profile_picture'
        ordering = ('created_at',)
