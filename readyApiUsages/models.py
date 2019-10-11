from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from datetime import datetime
from apps.models import (Apps)
from users.models import (Users)


# Ready Api Usage Bucket
class ReadyApiUsageBuckets(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    app = models.ForeignKey(Apps, on_delete=models.CASCADE)
    bucket = models.IntegerField("Bucket (Quota)", "bucket", default=100)
    usage = models.IntegerField("Usage (Calls Made)", "usage", default=0)
    threshold = models.IntegerField(
        "Threshold (Alert User of Usage)", "threshold", default=0)
    active = models.BooleanField("Is Active", "active", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flow_user_ready_api_usage_bucket'
        ordering = ('created_at',)
        verbose_name_plural = 'Ready Api Usage Buckets'


@receiver(post_save, sender=Apps)
def an_app_is_created(sender, instance, created, ** kwargs):
    if created:
        ReadyApiUsageBuckets.objects.create(
            app=instance, user_id=str(instance.user))
    else:
        pass
