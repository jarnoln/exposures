import datetime
import logging

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Exposure


logger = logging.getLogger(__name__)


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
    exposures = Exposure.objects.all().order_by('publish_date', 'category')
    if exposures:
        latest_date = exposures.last().publish_date
    else:
        latest_date = datetime.date.today()
    delta_month = datetime.timedelta(days=40)
    earliest_date = latest_date - delta_month
    exposures = exposures.filter(publish_date__gte=earliest_date)
    if exposures:
        first_date = exposures.first().publish_date
    else:
        first_date = earliest_date

    date_list = []
    date = first_date
    one_day = datetime.timedelta(days=1)
    while date <= latest_date:
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


def exposure_edit(request, exposure_id=0):
    errors = []
    message = ''
    exposure = None
    if exposure_id:
        exposure = get_object_or_404(Exposure, pk=exposure_id)

    if request.method == 'POST':
        category = request.POST['category']
        municipality = request.POST.get('municipality', '')
        location = request.POST.get('location', '')
        public_location = request.POST.get('public-location', '')
        news_link = request.POST.get('news-link', '')
        exposed_str = request.POST.get('exposed', '')
        quarantined_str = request.POST.get('quarantined', '')
        infected_str = request.POST.get('infected', '')
        publish_date_str = request.POST.get('publish-date', '')
        started_date_str = request.POST.get('started-date', '')
        started_time_hour = int(request.POST.get('started-time-hour', '0'))
        started_time_minute = int(request.POST.get('started-time-minute', '0'))
        ended_date_str = request.POST.get('ended-date', '')
        ended_time_hour = int(request.POST.get('ended-time-hour', '0'))
        ended_time_minute = int(request.POST.get('ended-time-minute', '0'))
        logger.debug(list(request.POST.items()))
        if not municipality:
            errors.append('Paikkakunta puuttuu')
        if not news_link:
            errors.append('Uutislinkki puuttuu')

        if not publish_date_str:
            errors.append('Julkaisupäivä puuttuu')
            publish_date = None
        else:
            publish_datetime = datetime.datetime.strptime(publish_date_str, '%Y-%m-%d')
            publish_date = publish_datetime.date()

        if not exposed_str:
            exposed_str = quarantined_str

        try:
            infected = int(infected_str)
        except ValueError:
            infected = 0

        try:
            quarantined = int(quarantined_str)
        except ValueError:
            quarantined = 0

        try:
            exposed = int(exposed_str)
        except ValueError:
            exposed = quarantined

        exposure_date = None
        started_date = None
        ended_date = None
        if started_date_str:
            started_date = datetime.datetime.strptime(started_date_str, '%Y-%m-%d')
            exposure_date = started_date
            started_date.hour = started_time_hour
            started_date.minute = started_time_minute
            if ended_date_str:
                ended_date = datetime.datetime.strptime(ended_date_str, '%Y-%m-%d')
            else:
                ended_date = started_date
            ended_date.hour = started_time_hour
            ended_date.minute = started_time_minute
            if ended_time_hour or ended_time_minute:
                ended_date.hour = ended_time_hour
                ended_date.minute = ended_time_minute

        if len(errors) == 0:
            exposure = Exposure(
                category=category,
                municipality=municipality,
                location=location,
                news_link=news_link,
                publish_date=publish_date,
                exposed_string=exposed_str,
                quarantined_total_string=quarantined_str,
                infected_string=infected_str,
            )
            if public_location:
                exposure.alert = True
            if exposed:
                exposure.exposed_total = exposed
            if quarantined:
                exposure.quarantined_total = quarantined
            if infected:
                exposure.infected_total = infected

            if exposure_date:
                exposure.exposure_date = exposure_date
            if started_date:
                exposure.exposure_started = started_date
            if ended_date:
                exposure.exposure_ended = ended_date
            exposure.save()
            message = 'Tallennettu: {}'.format(str(exposure))
        else:
            message = 'Tallennus ei onnistunut'

    context = {
        'exposure': exposure,
        'errors': errors,
        'message': message
    }
    return render(request, 'tables/exposure_edit.html', context=context)
