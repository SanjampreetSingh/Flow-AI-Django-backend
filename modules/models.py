from django.db import models
from datetime import datetime


# API Image Image path setting
def module_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/module_image/module_<id>/<filename>
    somelist = filename.split('.')  # spliting orignal file name into somelist
    extension = (somelist[-1])   # Getting last element of the list
    filename = str(instance.module.id) + '_' + \
        str(datetime.now()) + '.' + extension  # Re-writing file name
    return 'module_image/module_{0}/{1}'.format(instance.category.name, filename)


# Create your models here.
class Modules(models.Model):
    name = models.CharField("Name", "name", max_length=255)
    tagline = models.CharField("Tagline", "tagline", max_length=255)
    description = models.TextField(
        "Description", "description", null=True, blank=True)
    image = models.ImageField("Module Image", "image", upload_to=module_image_directory_path,
                              max_length=255, null=True, blank=True)
    active = models.BooleanField("Is Active", "active", default=True)
    reference_url = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_module'
        ordering = ('created_at',)

    def __str__(self):
        return "{}".format(self.name)
