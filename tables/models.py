from django.db import models


class Exposure(models.Model):
    municipality = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    level = models.CharField(max_length=100, default='', blank=True)
    news_link = models.URLField(blank=True)
    exposed_total = models.IntegerField(blank=True, default=0)
    quarantined_children = models.IntegerField(blank=True)
    quarantined_children_string = models.CharField(max_length=200, default='', blank=True)
    quarantined_adults = models.IntegerField(blank=True)
    quarantined_adults_string = models.CharField(max_length=200, default='', blank=True)
    quarantined_total = models.IntegerField(blank=True)
    quarantined_total_string = models.CharField(max_length=200, default='', blank=True)
    remote_status = models.CharField(max_length=100, default='', blank=True)
    publish_date = models.DateField(blank=True, null=True)  # When news of exposure was published
    exposure_date = models.DateField(blank=True, null=True)  # When exposure occurred (if known)
