from django.db import models
from datetime import datetime
from users.models import (Users)


#   Application Model Class
class Apps(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField("Name", "name", max_length=255)
    active = models.BooleanField("Is Active", "active", default=True)
    apikey_value = models.CharField(
        "Apikey Value", "apikey_value", max_length=100, null=True, blank=True)
    apikey_id = models.CharField(
        "Apikey ID", "apikey_id", max_length=100, null=True, blank=True)
    usage_plan_id = models.CharField(
        "Usage Plan ID", "usage_plan_id", max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_user_app'
        ordering = ('created_at',)

    def __str__(self):
        return "{}".format(self.name)


# App Image path setting
def app_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/app_image/app/user_<id>/<filename>
    somelist = filename.split('.')  # spliting orignal file name into somelist
    extension = (somelist[-1])   # Getting last element of the list
    filename = str(instance.user.id) + '_' + \
        str(datetime.now()) + '.' + extension  # Re-writing file name
    return 'user/app_image/app/user_{0}/{1}'.format(instance.user.id, filename)


# Avatar Model Class
class AppImage(models.Model):
    app = models.OneToOneField(
        Apps, on_delete=models.CASCADE)
    app_image = models.ImageField("App Image", "app_image", upload_to=app_image_directory_path,
                                  max_length=2083, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_user_app_image'
        ordering = ('created_at',)
