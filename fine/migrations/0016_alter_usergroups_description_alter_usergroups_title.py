# Generated by Django 4.1.4 on 2023-05-29 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fine', '0015_remove_registrationevents_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroups',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='usergroups',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
