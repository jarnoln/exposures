# Generated by Django 3.1.1 on 2020-09-25 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0011_auto_20200925_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
