# Generated by Django 4.1.4 on 2023-05-07 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fine', '0008_merge_20230506_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='theme',
            field=models.CharField(default='white', max_length=255),
        ),
    ]