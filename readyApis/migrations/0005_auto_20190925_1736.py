# Generated by Django 2.2.4 on 2019-09-25 12:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readyApis', '0004_readyapis_reference_api_call'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='readyapicategory',
            options={'ordering': ('created_at',), 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='readyapimedia',
            options={'ordering': ('created_at',), 'verbose_name_plural': 'Media'},
        ),
        migrations.AlterModelOptions(
            name='readyapis',
            options={'ordering': ('created_at',), 'verbose_name_plural': 'Ready Apis'},
        ),
        migrations.RenameField(
            model_name='readyapis',
            old_name='image',
            new_name='image_url',
        ),
        migrations.RemoveField(
            model_name='readyapis',
            name='cloud',
        ),
        migrations.AddField(
            model_name='readyapis',
            name='tag',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='readyapis',
            name='usage_plan',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Usage Plan'),
        ),
    ]
