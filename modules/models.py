from django.db import models
from datetime import datetime


# Modules model
class Modules(models.Model):
    name = models.CharField("Name", "name", max_length=255)
    tagline = models.CharField("Tagline", "tagline", max_length=255)
    description = models.TextField(
        "Description", "description", null=True, blank=True)
    image_url = models.CharField(
        "Image URL", "image_url", max_length=2083, null=True, blank=True)
    active = models.BooleanField("Is Active", "active", default=True)
    reference_url = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_module'
        ordering = ('created_at',)
        verbose_name_plural = 'Modules'

    def __str__(self):
        return "{}".format(self.name)
