from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.all_exposures, name='all_exposures'),
    path('municipalities/', views.exposures_by_municipality, name='exposures_by_municipality'),
    path('', views.exposures_by_category, name='exposures_by_category'),
]
