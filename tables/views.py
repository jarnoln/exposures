import datetime
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Exposure


def all_exposures(request):
    context = {
        'tab': 'all',
        'exposures': Exposure.objects.all().order_by('-publish_date')
    }
    return render(request, 'tables/all_exposures.html', context)


def alert_list(request):
    context = {
        'tab':  'alerts',
        'exposures': Exposure.objects.filter(alert=True).order_by('-exposure_started')
    }
    return render(request, 'tables/alert_list.html', context)


def exposures_by_category(request):
    exposures = Exposure.objects.all().order_by('-publish_date')
    template = loader.get_template('tables/exposures_by_category.html')
    context = {
        'tab': 'by_category',
        'schools': exposures.filter(category='school'),
        'daycares': exposures.filter(category='daycare'),
        'restaurants': exposures.filter(Q(category='restaurant') | Q(category='nightclub')),
        'others': exposures.filter(Q(category='other') | Q(category='transport'))
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


def get_exposures_by_date_list(long_format=False):
    today = datetime.date.today()
    month = datetime.timedelta(days=30)
    month_ago = today - month
    exposures = Exposure.objects.all().order_by('publish_date', 'category').filter(publish_date__gte=month_ago)
    first_date = exposures.first().publish_date
    date_list = []
    date = first_date
    one_day = datetime.timedelta(days=1)
    while date <= today:
        date_list.append(date)
        date = date + one_day

    exposures_by_date_array = []
    for date in date_list:
        date_key = date.strftime('%Y-%m-%d')
        exposure_list = []
        for index, exposure in enumerate(exposures.filter(publish_date=date).order_by('category')):
            exposure_dict = exposure.as_dict(long_format)
            exposure_dict['order'] = index + 1
            exposure_list.append(exposure_dict)

        exposures_by_date_array.append({
            'date_key': date_key,
            'display_date': date.strftime('%d.%m'),
            'exposures': exposure_list
        })
    return exposures_by_date_array


def exposures_by_date(request):
    return render(request, 'tables/exposures_by_date.html', {'tab': 'by_date'})


def api_exposures_by_date(request):
    exposures_by_date_list = get_exposures_by_date_list(long_format=True)
    return JsonResponse(exposures_by_date_list, safe=False)


def exposure_detail(request, exposure_id):
    exposure = get_object_or_404(Exposure, pk=exposure_id)
    return render(request, 'tables/exposure_detail.html', {'exposure': exposure})
