from django.db import models


class Exposure(models.Model):
    category = models.CharField(max_length=100, default='school', choices=[
        ('daycare', 'Daycare'),
        ('restaurant', 'Restaurant'),
        ('school', 'School'),
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
    remote_status = models.CharField(max_length=100, default='', blank=True)
    notes = models.TextField(default='', blank=True)
    publish_date = models.DateField(blank=True, null=True, help_text='When news of exposure was published')
    exposure_date = models.DateField(blank=True, null=True, help_text='When exposure occurred (if known)')

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
        elif self.category == 'restaurant':
            return 'ravintola'
        elif self.category == 'school':
            return 'koulu'
        elif self.category == 'other':
            return 'muu'
        return self.category

    def as_dict(self, long_format=False):
        exposure_dict = {
            'id': self.pk,
            'publish_date': self.publish_date.strftime('%Y-%m-%d'),
            'category': self.category,
            'news_link': self.news_link,
            'municipality': self.municipality
        }
        if long_format:
            exposure_dict['location'] = self.location  # Adding this breaks JSON parsing
        return exposure_dict

    def __str__(self):
        return '{}:{}:{}:{}:{}'.format(str(self.publish_date), self.category, self.municipality, self.location,
                                       str(self.news_link))

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
