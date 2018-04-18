import os, django, ast
from django.db import transaction
from django.db.models.query_utils import Q
from django.contrib.gis.geos import Point
from django.contrib.gis.gdal import SpatialReference, CoordTransform


@transaction.atomic
def update_fines(raw_tickets, geocoder_info=False):

    ticket_batch = []

    # preparo la matriz de transformación de coordenadas
    gcoord = SpatialReference(4326)
    mycoord = SpatialReference(25830)
    trans = CoordTransform(gcoord, mycoord)

    for i, raw_ticket in enumerate(raw_tickets):

        # Parseo los datos del objeto multa (están bastante "sucios")
        traffic_ticket = TrafficTicket()
        traffic_ticket.type = raw_ticket.calificacion.strip()
        traffic_ticket.address = raw_ticket.lugar.strip()
        traffic_ticket.month = int(raw_ticket.mes.strip())
        traffic_ticket.year = int(raw_ticket.anio.strip())
        traffic_ticket.timestamp = raw_ticket.hora.strip()
        traffic_ticket.tax = float(raw_ticket.imp_bol.strip())
        traffic_ticket.discount = (raw_ticket == 'SI')
        traffic_ticket.points = int(raw_ticket.puntos)
        traffic_ticket.informer = raw_ticket.denunciante.strip()
        traffic_ticket.fact = raw_ticket.hecho_bol.strip()
        traffic_ticket.speed_limit = float(raw_ticket.vel_limite.strip()) if raw_ticket.vel_limite.strip() else None
        traffic_ticket.speed_reg = float(raw_ticket.vel_circula.strip()) if raw_ticket.vel_circula.strip() else None

        if geocoder_info:  # si la información viene del geocoder, hay que extraer la info

            try:
                geoinfo = ast.literal_eval(raw_ticket.coordenada_y)
                lng = geoinfo[0]['geometry']['location']['lng']
                lat = geoinfo[0]['geometry']['location']['lat']

                # transformar las coordenadas de wgs84 (srid=4326) a etrs89 (srid=25830)
                pnt = Point(lng, lat, srid=4326)
                pnt.transform(trans)

                traffic_ticket.geom = pnt
                ticket_batch.append(traffic_ticket)
                raw_ticket.procesado = True
                raw_ticket.save()
            except:
                # algunos datos venían solo con coordenada y
                print('¡ERROR! ID: {}'.format(raw_ticket.id))
        else:
            traffic_ticket.geom = Point(float(raw_ticket.coordenada_x.strip()),
                                        float(raw_ticket.coordenada_y.strip()), srid=25830)
            ticket_batch.append(traffic_ticket)
            raw_ticket.procesado = True
            raw_ticket.save()

        if i % 500 == 0:
            TrafficTicket.objects.bulk_create(ticket_batch)
            ticket_batch = []
            print('{} of {}'.format(i, len(raw_tickets)))


if __name__ == "__main__":

    # inicio el entorno de django
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.sys.path.insert(0, parent_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madrid_geodjango.settings")
    django.setup()

    from madrid.models import TrafficTicket, MultasRaw

    # Paso 1: cargo las multas que contenían x,y
    raw_fines = MultasRaw.objects.filter(~Q(coordenada_x='           '))
    print('Updating {} fines with existing x, y'.format(len(raw_fines)))
    # update_fines(raw_fines)

    # Paso 2: cargo las multas geolocalizadas con el geocoder
    raw_fines = MultasRaw.objects.filter(
        Q(coordenada_x='           ') & ~Q(coordenada_y='           ') & ~Q(coordenada_y='1a vuelta - nada')
    )
    print('Updating {} geocoded fines'.format(len(raw_fines)))
    update_fines(raw_fines, geocoder_info=True)

    print('The end')
