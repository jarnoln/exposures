# Generated by Django 3.1.1 on 2020-09-01 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0003_exposure_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exposure',
            name='location',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
