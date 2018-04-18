from django.contrib.gis import admin
from django.urls import path

from madrid import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats_district/', views.stats_by_district, name='stats_by_district'),
    path('stats_neighborhood/', views.stats_by_neighborhood, name='stats_by_neighborhood'),
]
