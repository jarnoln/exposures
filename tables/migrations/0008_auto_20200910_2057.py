# Generated by Django 3.1.1 on 2020-09-10 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0007_informationlink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exposure',
            name='remote_status',
        ),
        migrations.AddField(
            model_name='exposure',
            name='alert',
            field=models.BooleanField(blank=True, default=False, help_text='If this should be placed in alert list'),
        ),
        migrations.AddField(
            model_name='exposure',
            name='exposure_endTime',
            field=models.DateTimeField(blank=True, help_text='End of exposure risk', null=True),
        ),
        migrations.AddField(
            model_name='exposure',
            name='exposure_startTime',
            field=models.DateTimeField(blank=True, help_text='Start of exposure risk', null=True),
        ),
        migrations.AlterField(
            model_name='exposure',
            name='category',
            field=models.CharField(choices=[('daycare', 'Daycare'), ('restaurant', 'Restaurant'), ('school', 'School'), ('transport', 'Transport'), ('other', 'Other')], default='school', max_length=100),
        ),
    ]
