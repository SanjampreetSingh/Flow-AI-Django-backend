from django.db import models
from datetime import datetime
from users.models import (Users)


# Profile Image path setting
def profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_image/user_<id>/<filename>
    somelist = filename.split('.')  # spliting orignal file name into somelist
    extension = (somelist[-1])   # Getting last element of the list
    filename = str(instance.user.id) + '_' + \
        str(datetime.now()) + '.' + extension  # Re-writing file name
    return 'user/profile_image/user_{0}/{1}'.format(instance.user.id, filename)


#   Profile Model Class
class Profiles(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHERS = 'O'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    )
    user = models.OneToOneField(
        Users, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(
        "First name", max_length=50, blank=True, null=True)
    middle_name = models.CharField(
        "Middle name", max_length=50, blank=True, null=True)
    last_name = models.CharField(
        "Last name", max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField("Address", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.user.id)

    def get_full_name(self):
        return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)

    class Meta:
        db_table = 'flow_user_profile'
        ordering = ('created_at',)

    # profile_image = models.ImageField("Profile Image", "profile_image", upload_to=profile_directory_path,
    #                                   max_length=2083, null=True, blank=True)
