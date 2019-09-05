# Generated by Django 2.2.4 on 2019-09-05 04:35

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('user_type', models.CharField(blank=True, choices=[('AD', 'Admin'), ('IN', 'Individual')], default='IN', max_length=2, null=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('complete', models.BooleanField(default=False, verbose_name='Profile Complete')),
                ('staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('admin', models.BooleanField(default=False, verbose_name='Admin')),
                ('verified', models.BooleanField(default=False, verbose_name='Verified')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'flow_user',
                'ordering': ('created_at',),
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]
