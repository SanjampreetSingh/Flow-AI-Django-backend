# Generated by Django 2.2.4 on 2019-09-12 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readyApis', '0002_readyapis_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='readyapimedia',
            name='url',
            field=models.CharField(blank=True, max_length=2083, null=True, verbose_name='URL'),
        ),
    ]