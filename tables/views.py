from django.http import HttpResponse
from django.template import loader

from .models import Exposure


def exposures_by_category(request):
    exposures = Exposure.objects.all().order_by('-publish_date')
    template = loader.get_template('tables/index.html')
    context = {
        'tab': 'by_category',
        'schools': exposures.filter(category='school'),
        'daycares': exposures.filter(category='daycare'),
        'restaurants': exposures.filter(category='restaurant')
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
