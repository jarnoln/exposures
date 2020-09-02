from django.urls import path

from . import views

urlpatterns = [
    path('municipalities/', views.exposures_by_municipality, name='exposures_by_municipality'),
    path('', views.exposures_by_category, name='exposures_by_category'),
]
