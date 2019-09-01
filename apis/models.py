from django.db import models
from datetime import datetime


#   API Category Model Class
class ApiCategory(models.Model):
    name = models.CharField("Name", "name", max_length=255)
    trial = models.BooleanField("Has Trial", "trial", default=False)
    active = models.BooleanField("Is Active", "active", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_api_category'
        ordering = ('created_at',)

    def __str__(self):
        return "{}".format(self.name)


#   API Model Class
class Api(models.Model):
    name = models.CharField("Name", "name", max_length=255)
    category = models.ForeignKey(ApiCategory, on_delete=models.CASCADE)
    trial = models.BooleanField("Has Trial", "trial", default=False)
    active = models.BooleanField("Is Active", "active", default=True)
    recommendations = models.SmallIntegerField(
        "Recommendations", "recommendations", default=0)
    price = models.FloatField("Price", "price", default=0.00)
    description = models.TextField(
        "Description", "description", null=True, blank=True)
    documentation = models.TextField(
        "Documentation", "documentation", null=True, blank=True)
    use_cases = models.TextField(
        "Use Cases", "use_cases", null=True, blank=True)
    image = models.CharField(
        "Image", "image", max_length=2083, null=True, blank=True)
    video = models.CharField(
        "Video", "video", max_length=2083, null=True, blank=True)
    cloud_url = models.CharField(max_length=255, unique=True)
    cloud = models.CharField(
        "Cloud Id", "cloud", max_length=2083, null=True, blank=True)
    apikey_stage = models.CharField(
        "Apikey Stage", "apikey_stage", max_length=2083, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_api'
        ordering = ('created_at',)

    def __str__(self):
        return "{}".format(self.name)


# API Image Image path setting
def api_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/api_image/api_<id>/<filename>
    somelist = filename.split('.')  # spliting orignal file name into somelist
    extension = (somelist[-1])   # Getting last element of the list
    filename = str(instance.api.id) + '_' + \
        str(datetime.now()) + '.' + extension  # Re-writing file name
    return 'api_image/api_{0}/{1}'.format(instance.category.name, filename)


class ApiImage(models.Model):
    api = models.ForeignKey(Api, on_delete=models.CASCADE)
    category = models.ForeignKey(ApiCategory, on_delete=models.CASCADE)
    image_url = models.CharField(
        "Image URL", "image_url", max_length=2083, blank=True, null=True)
    api_image = models.ImageField("API Image", "api_image", upload_to=api_image_directory_path,
                                  max_length=255, null=True, blank=True)
    trial = models.BooleanField("Is trial", "trial", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_api_images'
        ordering = ('created_at',)
