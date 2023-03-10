from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from users.models import (Users)


# Application Model Class
class Apps(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField("Name", "name", max_length=255)
    description = models.TextField(
        "Description", "description", null=True, blank=True)
    apikey_value = models.CharField(
        "Apikey Value", "apikey_value", max_length=100, null=True, blank=True)
    apikey_id = models.CharField(
        "Apikey ID", "apikey_id", max_length=100, null=True, blank=True)
    usage_plans = ArrayField(models.CharField(
        max_length=150, blank=True), blank=True, null=True)
    reference_url = models.SlugField()
    ready_apis = ArrayField(models.CharField(
        max_length=150, blank=True), blank=True, null=True)
    custom_apis = ArrayField(models.CharField(
        max_length=150, blank=True), blank=True, null=True)
    notebook = ArrayField(models.CharField(
        max_length=150, blank=True), blank=True, null=True)
    active = models.BooleanField("Is Active", "active", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_user_app'
        ordering = ('created_at',)
        verbose_name_plural = 'Apps'

    def __str__(self):
        return "{}".format(self.name)


# # App Image path setting
# def image_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/app_image/app/user_<id>/<filename>
#     somelist = filename.split('.')  # spliting orignal file name into somelist
#     extension = (somelist[-1])   # Getting last element of the list
#     filename = str(instance.user.id) + '_' + \
#         str(datetime.now()) + '.' + extension  # Re-writing file name
#     return 'user/app_image/user_{0}/{1}'.format(instance.user.id, filename)


# # App Image Model Class
# class AppImage(models.Model):
#     app = models.OneToOneField(
#         Apps, on_delete=models.CASCADE)
#     image = models.ImageField("Image", "image", upload_to=image_directory_path,
#                               max_length=2083, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'flow_user_app_image'
#         ordering = ('created_at',)
