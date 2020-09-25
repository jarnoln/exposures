import pytz

from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '{}:{}:{}'.format(self.order, self.name, self.title)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'categories'


class Exposure(models.Model):
    location_category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True, blank=True)
    category = models.CharField(max_length=100, default='school', choices=[
        ('daycare', 'Daycare'),
        ('restaurant', 'Restaurant'),
        ('nightclub', 'Nightclub'),
        ('school', 'School'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ])
    municipality = models.CharField(max_length=100)
    location = models.CharField(max_length=200, default='', blank=True)
    level = models.CharField(max_length=100, default='', blank=True)
    news_link = models.URLField(blank=True)
    infected_total = models.IntegerField(blank=True, default=0)
    infected_string = models.CharField(max_length=200, default='', blank=True)
    exposed_total = models.IntegerField(blank=True, default=0)
    exposed_string = models.CharField(max_length=200, default='', blank=True)
    quarantined_children = models.IntegerField(blank=True, null=True)
    quarantined_children_string = models.CharField(max_length=200, default='', blank=True)
    quarantined_adults = models.IntegerField(blank=True, null=True)
    quarantined_adults_string = models.CharField(max_length=200, default='', blank=True)
    quarantined_total = models.IntegerField(blank=True, null=True)
    quarantined_total_string = models.CharField(max_length=200, default='', blank=True)
    alert = models.BooleanField(default=False, blank=True, help_text="If this should be placed in alert list")
    notes = models.TextField(default='', blank=True)
    publish_date = models.DateField(blank=True, null=True, help_text='When news of exposure was published')
    exposure_date = models.DateField(blank=True, null=True, help_text='When exposure occurred (if known)')
    exposure_started = models.DateTimeField(blank=True, null=True, help_text='Start of exposure')
    exposure_ended = models.DateTimeField(blank=True, null=True, help_text='End of exposure')

    def display_infected(self):
        if self.infected_total:
            return str(self.infected_total)
        if self.infected_string:
            return self.infected_string
        return '?'

    def display_children(self):
        if self.quarantined_children:
            return str(self.quarantined_children)
        if self.quarantined_children_string:
            return self.quarantined_children_string
        return ''

    def display_adults(self):
        if self.quarantined_adults:
            return str(self.quarantined_adults)
        if self.quarantined_adults_string:
            return self.quarantined_adults_string
        return ''

    def display_total(self):
        if self.quarantined_total:
            return str(self.quarantined_total)
        if self.quarantined_total_string:
            return self.quarantined_total_string
        return '?'

    def display_category(self):
        if self.category == 'daycare':
            return 'päiväkoti'
        if self.category == 'nightclub':
            return 'yökerho'
        elif self.category == 'restaurant':
            return 'ravintola'
        elif self.category == 'school':
            return 'koulu'
        elif self.category == 'transport':
            return 'liikenneväline'
        elif self.category == 'other':
            return 'muu'
        return self.category

    def display_window(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        if not self.exposure_started:
            started_str = ''
        elif self.exposure_started.astimezone(tz).hour == 0 and self.exposure_started.astimezone(tz).minute == 0:
            # If time is not specified, show only date
            started_str = self.exposure_started.astimezone(tz).strftime('%d.%m')
        else:
            started_str = self.exposure_started.astimezone(tz).strftime('%d.%m %H:%M')

        if not self.exposure_ended:
            ended_str = ''
        elif self.exposure_ended.astimezone(tz).day == self.exposure_started.astimezone(tz).day:
            # If day is same, omit date
            if self.exposure_ended.astimezone(tz).hour == 0 and self.exposure_ended.astimezone(tz).minute == 0:
                # If time is not specified, show only start date
                ended_str = ''
            else:
                ended_str = self.exposure_ended.astimezone(tz).strftime('%H:%M')
        elif self.exposure_ended.astimezone(tz).day == self.exposure_started.astimezone(tz).day + 1 and \
                self.exposure_ended.astimezone(tz).hour <= 4:
            # If end time is next day but early morning hours, omit date
            ended_str = self.exposure_ended.astimezone(tz).strftime('%H:%M')
        elif self.exposure_ended.astimezone(tz).hour == 0 and self.exposure_ended.astimezone(tz).minute == 0:
            # If time is not specified, show only date
            ended_str = self.exposure_ended.astimezone(tz).strftime('%d.%m')
        else:
            # Otherwise show both date and time
            ended_str = self.exposure_ended.astimezone(tz).strftime('%d.%m %H:%M')

        if started_str and ended_str:
            return '{} - {}'.format(started_str, ended_str)
        elif started_str:
            return started_str
        return ended_str

    def as_dict(self, long_format=False):

        exposure_dict = {
            'id': self.pk,
            'category': self.location_category.name,
            'location_order': self.location_category.order,
            'municipality': self.municipality,
            'news_link': self.news_link,
            'publish_date': '',
            'total': self.display_total()
        }
        if self.publish_date:
            exposure_dict['publish_date'] = self.publish_date.strftime('%Y-%m-%d')

        if long_format:
            exposure_dict['location'] = self.location  # Adding this breaks JSON parsing
        return exposure_dict

    def __str__(self):
        return '{}:{}:{}:{}:{}'.format(str(self.publish_date), self.location_category.name, self.municipality,
                                       self.location, str(self.news_link))

    class Meta:
        ordering = ['-publish_date']


class InformationLink(models.Model):
    exposure = models.ForeignKey(Exposure, on_delete=models.CASCADE)
    link = models.URLField(blank=True)
    title = models.CharField(max_length=200, default='', blank=True)
    summary = models.TextField(default='', blank=True)
    publish_date = models.DateField(blank=True, null=True, help_text='When information was published')

    def __str__(self):
        return '{}:{}:{}:{}:{}'.format(str(self.publish_date), self.title, self.exposure.location, self.link)
