# Generated by Django 2.2.4 on 2019-09-25 05:36

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('apikey_value', models.CharField(blank=True, max_length=100, null=True, verbose_name='Apikey Value')),
                ('apikey_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Apikey ID')),
                ('usage_plans', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150), blank=True, null=True, size=None)),
                ('reference_url', models.SlugField(unique=True)),
                ('active_apis', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150), blank=True, null=True, size=None)),
                ('active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Apps',
                'db_table': 'flow_user_app',
                'ordering': ('created_at',),
            },
        ),
    ]
