import datetime
from django.test import TestCase
from tables.models import Exposure


class ExposureModelTest(TestCase):
    def test_can_save_and_load(self):
        exposure = Exposure(municipality='Tampere', location='Tampere University')
        exposure.save()
        self.assertEqual(Exposure.objects.all().count(), 1)
        self.assertEqual(Exposure.objects.all()[0], exposure)

    def test_string(self):
        exposure = Exposure.objects.create(
            municipality='Tampere',
            location='Tampere University',
            publish_date=datetime.date(year=2020, month=1, day=2)
        )
        self.assertEqual(str(exposure), '2020-01-02:school:Tampere:Tampere University:')

    def test_displays(self):
        exposure = Exposure.objects.create(municipality='Tampere', location='Tampere University')
        self.assertEqual(exposure.display_infected(), '?')
        self.assertEqual(exposure.display_total(), '?')
        self.assertEqual(exposure.display_category(), 'koulu')

    def test_display_window(self):
        exposure = Exposure.objects.create(municipality='Tampere', location='Tampere University')
        self.assertEqual(exposure.display_window(), '')
        exposure.exposure_started = datetime.datetime(year=2020, month=1, day=2, hour=0, minute=0)
        self.assertEqual(exposure.display_window(), '02.01')
        exposure.exposure_started = datetime.datetime(year=2020, month=1, day=2, hour=12, minute=30)
        self.assertEqual(exposure.display_window(), '02.01 12:30')
        exposure.exposure_ended = datetime.datetime(year=2020, month=1, day=2, hour=13, minute=30)
        self.assertEqual(exposure.display_window(), '02.01 12:30 - 13:30')
        exposure.exposure_started = datetime.datetime(year=2020, month=1, day=2, hour=23, minute=0)
        exposure.exposure_ended = datetime.datetime(year=2020, month=1, day=3, hour=1, minute=0)
        self.assertEqual(exposure.display_window(), '02.01 23:00 - 01:00')
        exposure.exposure_ended = datetime.datetime(year=2020, month=1, day=3, hour=9, minute=0)
        self.assertEqual(exposure.display_window(), '02.01 23:00 - 03.01 09:00')

    def test_as_dictionary(self):
        exposure = Exposure.objects.create(municipality='Tampere', location='Tampere University')
        d = exposure.as_dict(long_format=True)
        self.assertEqual(d['id'], exposure.id)
        self.assertEqual(d['municipality'], 'Tampere')
        self.assertEqual(d['category'], 'school')
        self.assertEqual(d['location'], 'Tampere University')
        self.assertEqual(d['news_link'], '')
        self.assertEqual(d['publish_date'], '')
