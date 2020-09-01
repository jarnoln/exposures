from django.http import HttpResponse
from django.template import loader

from .models import Exposure


def index(request):
    exposures = Exposure.objects.all()
    template = loader.get_template('tables/index.html')
    context = {
        'exposures': exposures
    }
    return HttpResponse(template.render(context, request))
