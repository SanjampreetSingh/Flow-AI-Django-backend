# Generated by Django 2.2.4 on 2019-09-21 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readyApis', '0003_readyapimedia_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='readyapis',
            name='reference_api_call',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
