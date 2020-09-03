from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.all_exposures, name='all_exposures'),
    path('dates/', views.exposures_by_date, name='exposures_by_date'),
    path('municipalities/', views.exposures_by_municipality, name='exposures_by_municipality'),
    path('', views.exposures_by_category, name='exposures_by_category'),
]
