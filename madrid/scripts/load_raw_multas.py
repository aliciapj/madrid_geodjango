import csv, os, django

# Auto-generated `LayerMapping` dictionary for Multas model
multas_mapping = {
    'calificacion': 'CALIFICACION',
    'lugar': 'LUGAR',
    'mes': 'MES',
    'anio': 'ANIO',
    'hora': 'HORA',
    'imp_bol': 'IMP_BOL',
    'descuento': 'DESCUENTO',
    'puntos': 'PUNTOS',
    'denunciante': 'DENUNCIANTE',
    'hecho_bol': 'HECHO-BOL',
    'vel_limite': 'VEL_LIMITE',
    'vel_circula': 'VEL_CIRCULA',
    'coordenada_x': 'COORDENADA_X',
    'coordenada_y': 'COORDENADA_Y',
    'geom': 'NONE',
}

if __name__ == "__main__":

    # inicio el entorno de django
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.sys.path.insert(0, parent_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madrid_geodjango.settings")
    django.setup()

    from madrid.models import MultasRaw

    # abro el fichero csv
    path = os.path.join(os.path.dirname(__file__), 'data', '201711_detalle.csv'),

    with open(path, encoding='iso-8859-1') as f:
        reader = csv.reader(f, delimiter=';')

        # me salto las cabeceras
        next(reader, None)  # skip the headers

        # creo el objeto en la base de datos con el orm de django
        for row in reader:
            _, created = MultasRaw.objects.get_or_create(
                calificacion=row[0],
                lugar=row[1],
                mes=row[2],
                anio=row[3],
                hora=row[4],
                imp_bol=row[5],
                descuento=row[6],
                puntos=row[7],
                denunciante=row[8],
                hecho_bol=row[9],
                vel_limite=row[10],
                vel_circula=row[11],
                coordenada_x=row[12],
                coordenada_y=row[13]
            )
