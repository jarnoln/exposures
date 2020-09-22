from django.urls import path

from . import views

urlpatterns = [
    path('api/exposures_by_date/', views.api_exposures_by_date, name='api_exposures_by_date'),
    path('exposure/<int:exposure_id>/', views.exposure_detail, name='exposure_detail'),
    path('all/', views.all_exposures, name='all_exposures'),
    path('dates/', views.exposures_by_date, name='exposures_by_date'),
    path('municipalities/', views.exposures_by_municipality, name='exposures_by_municipality'),
    path('categories/', views.exposures_by_category, name='exposures_by_category'),
    path('exposure/add/', views.exposure_edit, name='add_exposure'),
    path('', views.alert_list, name='alert_list'),
]
