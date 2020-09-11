import datetime
from django.test import TestCase
from tables.models import Exposure
from django.urls import reverse


class AlertListTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('alert_list'), '/')

    def test_uses_correct_template(self):
        response = self.client.get(reverse('alert_list'))
        self.assertTemplateUsed(response, 'tables/base.html')
        self.assertTemplateUsed(response, 'tables/alert_list.html')

    def test_default_content(self):
        response = self.client.get(reverse('alert_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tab'], 'alerts')
        self.assertEqual(response.context['exposures'].count(), 0)

        exposure = Exposure.objects.create(municipality='Tampere', location='University')
        response = self.client.get(reverse('alert_list'))
        self.assertEqual(response.context['exposures'].count(), 0)

        exposure.alert = True
        exposure.save()
        response = self.client.get(reverse('alert_list'))
        self.assertEqual(response.context['exposures'].count(), 1)


class ExposuresByCategoryTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('exposures_by_category'), '/categories/')

    def test_uses_correct_template(self):
        response = self.client.get(reverse('exposures_by_category'))
        self.assertTemplateUsed(response, 'tables/base.html')
        self.assertTemplateUsed(response, 'tables/exposures_by_category.html')

    def test_default_content(self):
        response = self.client.get(reverse('exposures_by_category'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tab'], 'by_category')
        self.assertEqual(response.context['schools'].count(), 0)
        self.assertEqual(response.context['daycares'].count(), 0)
        self.assertEqual(response.context['restaurants'].count(), 0)
        self.assertEqual(response.context['others'].count(), 0)


class ExposuresByMunicipalityTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('exposures_by_municipality'), '/municipalities/')

    def test_uses_correct_template(self):
        response = self.client.get(reverse('exposures_by_municipality'))
        self.assertTemplateUsed(response, 'tables/base.html')
        self.assertTemplateUsed(response, 'tables/exposures_by_municipality.html')

    def test_default_content(self):
        response = self.client.get(reverse('exposures_by_municipality'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tab'], 'by_municipality')
        self.assertEqual(len(response.context['municipalities']), 0)
        self.assertEqual(len(response.context['exposures_by_municipality']), 0)


class ExposuresByDateTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('exposures_by_date'), '/dates/')

    def test_uses_correct_template(self):
        response = self.client.get(reverse('exposures_by_date'))
        self.assertTemplateUsed(response, 'tables/base.html')
        self.assertTemplateUsed(response, 'tables/exposures_by_date.html')

    def test_default_content(self):
        response = self.client.get(reverse('exposures_by_date'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tab'], 'by_date')
