from django.contrib.gis.db import models as gismodel
from django.db import models


class District(gismodel.Model):
    name = gismodel.CharField(max_length=50)
    code = gismodel.CharField(max_length=2)
    geom = gismodel.MultiPolygonField()


class Neighborhood(gismodel.Model):
    code = gismodel.CharField(max_length=4)
    code2 = gismodel.CharField(max_length=12)
    name = gismodel.CharField(max_length=50)
    district_name = gismodel.CharField(max_length=50)
    district_code = gismodel.CharField(max_length=2)
    geom = gismodel.MultiPolygonField()


class MultasRaw(models.Model):
    calificacion = models.TextField()  # TIPO DE INFRACCION (M. GRAVE, LEVE..)
    lugar = models.TextField()    # LUGAR DE INFRACCION
    mes = models.TextField()  # MES DE DENUNCIA
    anio = models.TextField()  # ANIO DENUNCIA
    hora = models.TextField()  # HORA DENUNCIA MM/YYYY
    imp_bol = models.TextField()  # IMPORTE DEL BOLETÍN (2 DECIMALES)
    descuento = models.TextField()  # DESCUENTO 'SI', 'NO'
    puntos = models.TextField()  # PUNTOS DETRAIDOS
    denunciante = models.TextField()  # DENUNCIANTE
    hecho_bol = models.TextField()  # HECHO DENUNCIADO
    vel_limite = models.TextField()  # VELOCIDAD LIMITE (SI ES RADAR)
    vel_circula = models.TextField()  # VELOCIDAD MEDIDA (SI ES RADAR)
    coordenada_x = models.TextField()  # COORDENADA X
    coordenada_y = models.TextField()  # COORDENADA Y
    procesado = models.BooleanField(default=False)


class TrafficTicket(gismodel.Model):
    type = gismodel.TextField(max_length=10)  # TIPO DE INFRACCION (M. GRAVE, LEVE..)
    address = gismodel.TextField(max_length=100)    # LUGAR DE INFRACCION
    month = gismodel.IntegerField()  # MES DE DENUNCIA
    year = gismodel.IntegerField()  # ANIO DENUNCIA
    timestamp = gismodel.TextField(max_length=8)  # HORA DENUNCIA MM/YYYY
    tax = gismodel.FloatField()  # IMPORTE DEL BOLETÍN (2 DECIMALES)
    discount = gismodel.BooleanField()  # DESCUENTO 'SI', 'NO'
    points = gismodel.IntegerField()  # PUNTOS DETRAIDOS
    informer = gismodel.TextField(max_length=50)  # DENUNCIANTE
    fact = gismodel.TextField(max_length=500)  # HECHO DENUNCIADO
    speed_limit = gismodel.FloatField(null=True)  # VELOCIDAD LIMITE (SI ES RADAR)
    speed_reg = gismodel.FloatField(null=True)  # VELOCIDAD MEDIDA (SI ES RADAR)
    geocoder_info = gismodel.TextField(max_length=1000)  # INFORMACIÓN DEL GEOCODER
    geom = gismodel.PointField(srid=4326)
