from django.urls import path

from . import views

urlpatterns = [
    path('municipalities/', views.exposures_by_municipality, name='exposures_by_municipality'),
    path('categories/', views.exposures_by_category, name='exposures_by_category'),
    path('', views.all_exposures, name='all_exposures'),
]
