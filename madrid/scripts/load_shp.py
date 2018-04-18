import os, django

district_shp = 'madrid/data/DISTRITOS.shp'
neiborhood_shp = 'madrid/data/Barrios.shp'

# Auto-generated `LayerMapping` dictionary for Distrito model
district_mapping = {
    'name': 'NOMBRE',
    'code': 'CODDISTRIT',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for Barrio model
neighborhood_mapping = {
    'district_name': 'NOMDIS',
    'code': 'CODBAR',
    'district_code': 'CODDISTRIT',
    'code2': 'CODBARRIO',
    'name': 'NOMBRE',
    'geom': 'MULTIPOLYGON',
}

if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.sys.path.insert(0, parent_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madrid_geodjango.settings")
    django.setup()

    from django.contrib.gis.utils import LayerMapping
    from madrid.models import Neighborhood, neighborhood_mapping

    lm = LayerMapping(
        Neighborhood, neiborhood_shp, neighborhood_mapping,
        transform=True, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=True)