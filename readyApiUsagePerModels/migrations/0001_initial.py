# Generated by Django 2.2.4 on 2019-10-19 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('readyApis', '0002_auto_20190928_1222'),
        ('apps', '0003_auto_20190928_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadyApiUsagePerModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.IntegerField(default=0, verbose_name='Usage (Calls Made)')),
                ('active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readyApis.ReadyApis')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Apps')),
            ],
            options={
                'verbose_name_plural': 'Ready Api Usage Per Models',
                'db_table': 'flow_user_ready_api_usage_per_models',
                'ordering': ('created_at',),
            },
        ),
    ]