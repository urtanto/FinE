# Generated by Django 4.1.5 on 2023-04-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fine', '0004_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='finish_day',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_day',
            field=models.DateField(),
        ),
    ]