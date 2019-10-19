from django.db import models
from datetime import datetime
from apps.models import (Apps)
from readyApis.models import (ReadyApis)


# Ready Api Usage Bucket Per Models
class ReadyApiUsagePerModels(models.Model):
    api = models.ForeignKey(ReadyApis, on_delete=models.CASCADE)
    app = models.ForeignKey(Apps, on_delete=models.CASCADE)
    usage = models.IntegerField("Usage (Calls Made)", "usage", default=0)
    active = models.BooleanField("Is Active", "active", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flow_user_ready_api_usage_per_models'
        ordering = ('created_at',)
        verbose_name_plural = 'Ready Api Usage Per Models'
