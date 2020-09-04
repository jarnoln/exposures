# Generated by Django 3.1.1 on 2020-09-04 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0006_auto_20200904_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformationLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True)),
                ('title', models.CharField(blank=True, default='', max_length=200)),
                ('summary', models.TextField(blank=True, default='')),
                ('publish_date', models.DateField(blank=True, help_text='When information was published', null=True)),
                ('exposure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.exposure')),
            ],
        ),
    ]
