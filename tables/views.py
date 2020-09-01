from django.http import HttpResponse
from django.template import loader

from .models import Exposure


def index(request):
    exposures = Exposure.objects.all().order_by('publish_date')
    schools = exposures.filter(category='school')
    daycares = exposures.filter(category='daycare')
    template = loader.get_template('tables/index.html')
    context = {
        'schools': schools,
        'daycares': daycares
    }
    return HttpResponse(template.render(context, request))
