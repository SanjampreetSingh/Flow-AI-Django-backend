# Generated by Django 2.2.4 on 2019-09-19 06:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readyApps', '0002_auto_20190919_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readyapps',
            name='ready_apis',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150), blank=True, size=None),
        ),
    ]