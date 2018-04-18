from django.contrib.gis import admin

from .models import District, Neighborhood, TrafficTicket

admin.site.register(District, admin.GeoModelAdmin)
admin.site.register(TrafficTicket, admin.GeoModelAdmin)
admin.site.register(Neighborhood, admin.GeoModelAdmin)
