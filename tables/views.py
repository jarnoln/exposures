import datetime
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import Exposure


def all_exposures(request):
    template = loader.get_template('tables/all_exposures.html')
    context = {
        'tab': 'all',
        'exposures': Exposure.objects.all().order_by('-publish_date')
    }
    return HttpResponse(template.render(context, request))


def exposures_by_category(request):
    exposures = Exposure.objects.all().order_by('-publish_date')
    template = loader.get_template('tables/exposures_by_category.html')
    context = {
        'tab': 'by_category',
        'schools': exposures.filter(category='school'),
        'daycares': exposures.filter(category='daycare'),
        'restaurants': exposures.filter(category='restaurant'),
        'others': exposures.filter(category='other')
    }
    return HttpResponse(template.render(context, request))


def exposures_by_municipality(request):
    exposures = Exposure.objects.all().order_by('-publish_date')
    municipalities = Exposure.objects.values_list('municipality', flat=True).order_by('municipality')
    exposures_by_municipality_dict = {}
    for municipality in municipalities:
        exposures_by_municipality_dict[municipality] = exposures.filter(municipality=municipality)

    template = loader.get_template('tables/exposures_by_municipality.html')
    context = {
        'tab': 'by_municipality',
        'municipalities': municipalities,
        'exposures_by_municipality': exposures_by_municipality_dict
    }
    return HttpResponse(template.render(context, request))


def get_exposures_by_date_dict(long_format=False):
    exposures = Exposure.objects.all().order_by('publish_date')
    # publish_dates = Exposure.objects.values_list('publish_date', flat=True)
    first_date = exposures.first().publish_date
    today = datetime.date.today()
    date_list = []
    date = first_date
    one_day = datetime.timedelta(days=1)
    while date <= today:
        date_list.append(date)
        date = date + one_day

    exposures_by_date_dict = {}
    for date in date_list:
        date_key = date.strftime('%Y-%m-%d')
        exposures_by_date_dict[date_key] = {
            'display_date': date.strftime('%d.%m'),
            'exposures': []
        }
        for exposure in exposures.filter(publish_date=date):
            exposures_by_date_dict[date_key]['exposures'].append(exposure.as_dict(long_format))
    return exposures_by_date_dict


def exposures_by_date(request):
    template = loader.get_template('tables/exposures_by_date.html')
    context = {
        'tab': 'by_date'
    }
    return HttpResponse(template.render(context, request))


def api_exposures_by_date(request):
    exposures_by_date_dict = get_exposures_by_date_dict(long_format=True)
    return JsonResponse(exposures_by_date_dict)
