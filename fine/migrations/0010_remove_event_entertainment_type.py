# Generated by Django 4.1.4 on 2023-05-18 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fine', '0009_user_theme_usergroups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='entertainment_type',
        ),
    ]