from django.db import models


# Create your models here.
class Victim(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    age = models.IntegerField(verbose_name="Edad")
    age_max = models.IntegerField(verbose_name="Edad Max")
    occupation = models.TextField(verbose_name="Ocupacíon")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "victima"
        verbose_name_plural = "victimas"
        ordering = ['name']

    def __str__(self):
        return self.name


class Aggressor(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    age = models.IntegerField(verbose_name="Edad")
    age_max = models.IntegerField(verbose_name="Edad Max")
    occupation = models.TextField(verbose_name="Ocupacíon")
    victimRel = models.TextField(verbose_name="Relacion con victima")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "agresor"
        verbose_name_plural = "agresores"
        ordering = ['name']

    def __str__(self):
        return self.name


class TypeAggression(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "tipo_agresión"
        verbose_name_plural = "tipo_agreciones"
        ordering = ['name']

    def __str__(self):
        return self.name



class Region(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "regiones"
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    region = models.ForeignKey(Region, verbose_name="Region", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "distrito"
        verbose_name_plural = "distritos"
        ordering = ['name']

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    district = models.ForeignKey(District, verbose_name="Distrito", on_delete=models.CASCADE)
    code = models.IntegerField(verbose_name="Codigo Municipio", )
    region = models.ForeignKey(Region, verbose_name="Region", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "municipio"
        verbose_name_plural = "municipios"
        ordering = ['name']

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    municipality = models.ForeignKey(Municipality, verbose_name="Municipio", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "lugar"
        verbose_name_plural = "lugares"
        ordering = ['name']

    def __str__(self):
        return self.name


class Aggression(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=200)
    victim = models.OneToOneField(Victim, on_delete=models.CASCADE, verbose_name="Victima")
    aggressors = models.ForeignKey(Aggressor, on_delete=models.CASCADE, verbose_name="Agresores")
    observations = models.CharField(verbose_name="Observaciones", max_length=200)
    informer = models.CharField(verbose_name="Denunciante", max_length=200)
    source = models.CharField(verbose_name="Fuente", max_length=200)
    quantity = models.IntegerField(verbose_name="Cantidad")
    detail = models.CharField(verbose_name="Detalle", max_length=200)
    alleged_mobile = models.CharField(verbose_name="Presunto_Movil", max_length=200)
    aggression_type = models.ForeignKey(TypeAggression, verbose_name="Tipo_agresion", on_delete=models.CASCADE)
    sites = models.ForeignKey(Site, verbose_name="Lugar", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "agreción"
        verbose_name_plural = "agreciones"
        ordering = ['name']

    def __str__(self):
        return self.name
