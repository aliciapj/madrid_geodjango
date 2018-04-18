import googlemaps, os, django


gmaps = googlemaps.Client(key='your key here')


if __name__ == "__main__":

    # inicio el entorno de django
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.sys.path.insert(0, parent_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madrid_geodjango.settings")
    django.setup()

    from madrid.models import MultasRaw

    # filtro las multas sin coordenadas
    multas = MultasRaw.objects.filter(coordenada_y='           ')

    i = 0

    for multa in multas:

        # preparo la dirección para hacerselo "más fácil" al geocoder
        # 1. añado la ciudad (Madrid) y el país (Spain) a la dirección
        # 2. elimino los espacios en blanco innecesarios
        # 3. reemplazo los guiones bajos y "SN" por espacios en blanco
        address = '{}, Madrid, Spain'.format(multa.lugar.strip().replace('_', ' ').replace('SN', ' '))
        print('Geocoding -- {}'.format(address))

        # geocodifico
        geocode_result = gmaps.geocode(address)
        print('\t{}'.format(geocode_result))

        # guardo el resultado del geocoding
        multa.coordenada_y = str(geocode_result)
        multa.save()

        # trazo el número de peticiones que llevo
        i += 1
        print('******* {} requests'.format(i))
