import googlemaps, os, django
from django.db.models.aggregates import Count


gmaps = googlemaps.Client(key='your key here')


if __name__ == "__main__":

    # inicio el entorno de django
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.sys.path.insert(0, parent_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madrid_geodjango.settings")
    django.setup()

    from madrid.models import MultasRaw

    # filtro las multas sin coordenadas
    # agrupadas por lugar
    # ordenadas por cantidad descendiente (para empezar por las que tienen más multas)
    lugares = MultasRaw.objects.filter(coordenada_y='           ')\
        .values('lugar').annotate(Count('lugar'))\
        .order_by('-lugar__count')

    i = 0

    for lugar in lugares:

        # preparo la dirección para hacerselo "más fácil" al geocoder
        # 1. añado la ciudad (Madrid) y el país (Spain) a la dirección
        # 2. elimino los espacios en blanco innecesarios
        # 3. reemplazo los guiones bajos y "SN" por espacios en blanco
        address = '{}, Madrid, Spain'.format(lugar['lugar'].strip().replace('_', ' ').replace('SN', ' '))
        print('Geocoding -- {}'.format(address))

        # geocodifico
        geocode_result = gmaps.geocode(address)
        print('\t{}'.format(geocode_result))

        # actualizo todas las multas con esa dirección
        multas = MultasRaw.objects.filter(lugar=lugar['lugar']).update(coordenada_y=geocode_result)

        i += 1
        # trazo el número de peticiones que llevo y el número de multas actualizadas
        print('******* {} requests - {} updated'.format(i, len(multas)))
