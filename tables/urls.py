from django.urls import path

from . import views

urlpatterns = [
    path('api/exposures_by_date/', views.api_exposures_by_date, name='api_exposures_by_date'),
    path('exposure/<int:exposure_id>/', views.exposure_detail, name='exposure_detail'),
    path('exposure/add/', views.exposure_edit, name='add_exposure'),
    path('alerts/', views.alert_list, name='alert_list'),
    path('all/', views.all_exposures, name='all_exposures'),
    path('municipalities/', views.exposures_by_municipality, name='exposures_by_municipality'),
    path('categories/', views.exposures_by_category, name='exposures_by_category'),
    path('', views.exposures_by_date, name='exposures_by_date'),
]
