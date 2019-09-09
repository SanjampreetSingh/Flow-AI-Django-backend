# Generated by Django 2.2.4 on 2019-09-08 05:32

from django.db import migrations, models
import modules.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('tagline', models.CharField(max_length=255, verbose_name='Tagline')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to=modules.models.module_image_directory_path, verbose_name='Module Image')),
                ('active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('reference_url', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'flow_module',
                'ordering': ('created_at',),
            },
        ),
    ]