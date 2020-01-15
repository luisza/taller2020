from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class BaseInsertModels(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

# Create your models here.
class Victim(BaseInsertModels):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    age = models.IntegerField(verbose_name="Edad", validators=[
        MinValueValidator(1), MaxValueValidator(120)
    ], null=True)
    age_max = models.IntegerField(verbose_name="Edad Max", null=True)
    occupation = models.TextField(verbose_name="Ocupacíon")


    class Meta:
        verbose_name = "victima"
        verbose_name_plural = "victimas"
        ordering = ['name']




class Aggressor(BaseInsertModels):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    age = models.CharField(max_length=50, verbose_name="Edad", null=True)
    occupation = models.TextField(verbose_name="Ocupacíon")
    victimRel = models.TextField(verbose_name="Relacion con victima", null=True)

    class Meta:
        verbose_name = "agresor"
        verbose_name_plural = "agresores"
        ordering = ['name']




class TypeAggression(BaseInsertModels):
    name = models.CharField(verbose_name="Nombre", max_length=200)

    class Meta:
        verbose_name = "tipo_agresión"
        verbose_name_plural = "tipo_agreciones"
        ordering = ['name']




class Region(BaseInsertModels):
    name = models.CharField(verbose_name="Nombre", max_length=200)

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "regiones"
        ordering = ['name']


class District(BaseInsertModels):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    region = models.ForeignKey(Region, verbose_name="Region", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "distrito"
        verbose_name_plural = "distritos"
        ordering = ['name']

class Municipality(BaseInsertModels):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    district = models.ForeignKey(District, verbose_name="Distrito", on_delete=models.CASCADE)
    code = models.IntegerField(verbose_name="Codigo Municipio", )
    region = models.ForeignKey(Region, verbose_name="Region", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "municipio"
        verbose_name_plural = "municipios"
        ordering = ['name']


class Site(BaseInsertModels):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    municipality = models.ForeignKey(Municipality, verbose_name="Municipio",
                                     on_delete=models.CASCADE)

    class Meta:
        verbose_name = "lugar"
        verbose_name_plural = "lugares"
        ordering = ['name']



class Aggression(BaseInsertModels):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    victim = models.OneToOneField(Victim, on_delete=models.CASCADE, verbose_name="Victima")
    aggressors = models.ForeignKey(Aggressor, on_delete=models.SET_NULL, null=True, verbose_name="Agresores")
    observations = models.CharField(verbose_name="Observaciones", max_length=200)
    informer = models.CharField(verbose_name="Denunciante", max_length=200, null=True)
    source = models.CharField(verbose_name="Fuente", max_length=200)
    quantity = models.IntegerField(verbose_name="Cantidad")
    detail = models.CharField(verbose_name="Detalle", max_length=200, null=True)
    alleged_mobile = models.CharField(verbose_name="Presunto_Movil", max_length=200, null=True)
    aggression_type = models.ForeignKey(TypeAggression, verbose_name="Tipo_agresion", on_delete=models.CASCADE)
    sites = models.ForeignKey(Site, verbose_name="Lugar", on_delete=models.CASCADE)
    year = models.SmallIntegerField(verbose_name="Año")
    note_date = models.DateField(verbose_name="Fecha de la nota")

    class Meta:
        verbose_name = "agresión"
        verbose_name_plural = "agresiones"
        ordering = ['name']

