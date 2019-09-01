from django.db import models
from datetime import datetime


# Plan Model
class Plans(models.Model):
    name = models.CharField("Plan Name", "name", max_length=255, unique=True)
    operations = models.IntegerField("Operations", "operations", default=0)
    price = models.FloatField("Price", "price", default=0.00)
    total_count = models.IntegerField(default=0)
    quota_limit = models.IntegerField(default=0)
    burst_limit = models.IntegerField(default=0)
    rate_limit = models.FloatField(default=0.00)
    active = models.BooleanField("Is Active", "active", default=True)
    content = models.TextField(blank=True, null=True)
    plan_razor_id = models.CharField(
        "Razor Plan ID", "plan_razor_id", max_length=255, blank=True, null=True)
    plan_aws_id = models.CharField(
        "AWS Plan ID", "plan_aws_id", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flow_plan'
        ordering = ('operations',)

    def __str__(self):
        return str("{}".format(self.name))
