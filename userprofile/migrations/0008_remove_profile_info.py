# Generated by Django 4.0.1 on 2022-03-29 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_profile_info_alter_profile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='info',
        ),
    ]
