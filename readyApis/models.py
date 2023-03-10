from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField


# Ready API Category Model Class
class ReadyApiCategory(models.Model):
    name = models.CharField("Name", "name", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_ready_api_category'
        ordering = ('created_at',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return "{}".format(self.name)


# Ready API Model Class
class ReadyApis(models.Model):
    name = models.CharField("Name", "name", max_length=255)
    category = models.ForeignKey(ReadyApiCategory, on_delete=models.CASCADE)
    active = models.BooleanField("Is Active", "active", default=True)
    tagline = models.CharField("Tagline", "tagline", max_length=255)
    description = models.TextField(
        "Description", "description", null=True, blank=True)
    image_url = models.CharField(
        "Image", "image_url", max_length=2083, null=True, blank=True)
    cloud_url = models.CharField(max_length=255, unique=True)
    usage_plan_id = models.CharField(
        "Usage Plan", "usage_plan_id", max_length=255, null=True, blank=True)
    use_cases = models.TextField(
        "Use Cases", "use_cases", null=True, blank=True)
    apikey_stage = models.CharField(
        "Apikey Stage", "apikey_stage", max_length=2083, null=True, blank=True)
    recommendations = models.SmallIntegerField(
        "Recommendations", "recommendations", default=0)
    price = models.FloatField("Price", "price", default=0.00)
    tag = ArrayField(models.CharField(
        max_length=150, blank=True), blank=True, null=True)
    reference_url = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_ready_api'
        ordering = ('created_at',)
        verbose_name_plural = 'Ready Apis'

    def __str__(self):
        return "{}".format(self.name)


# Ready API media path setting
def media_directory_path(instance, filename):
    somelist = filename.split('.')  # spliting orignal file name into somelist
    extension = (somelist[-1])   # Getting last element of the list
    filename = str(instance.api.id) + '_' + \
        str(datetime.now()) + '.' + extension  # Re-writing file name
    return 'api/ready_api_media/api_{0}/{1}/{2}'.format(instance.category.name, extension, filename)


# Ready API Media Model Class
class ReadyApiMedia(models.Model):
    category = models.ForeignKey(ReadyApiCategory, on_delete=models.CASCADE)
    media = models.FileField(
        "Media", "media", upload_to=media_directory_path, max_length=255, null=True, blank=True)
    url = models.CharField(
        "URL", "url", max_length=2083, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_ready_api_media'
        ordering = ('created_at',)
        verbose_name_plural = 'Media'
