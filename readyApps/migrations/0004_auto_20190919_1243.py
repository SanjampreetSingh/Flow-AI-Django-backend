# Generated by Django 2.2.4 on 2019-09-19 07:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readyApps', '0003_auto_20190919_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readyapps',
            name='ready_apis',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150), blank=True, null=True, size=None),
        ),
    ]
