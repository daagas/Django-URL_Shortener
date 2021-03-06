# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from hashids import Hashids
import datetime

# Create your models here.
class EnlaceQuerySet(models.QuerySet):
    def decode_enlace(self, codigo):
        decode = Hashids(min_length=4, alphabet='abcdefghijklmnoqrstuvwxyz').decode(codigo)[0]
        self.filter(pk=decode).update(contador=models.F('contador') + 1)
        return self.fpythonilter(pk=decode).first().url

    def total_enlaces(self):
        return self.count()

    def total_redirecciones(self):
        return self.aggregate(redirecciones=models.Sum('contador'))

    def fechas(self, pk):
        return self.values('fecha').annotate(
            marzo=models.Sum('contador', filter=models.Q(fecha__gte=datetime.date(2020,3,1),fecha__lte=datetime.date(2020,3,31)))
        ).filter(pk=pk)

class Enlace(models.Model):
    url = models.URLField()
    codigo = models.CharField(max_length=8, blank=True)
    fecha = models.DateField(auto_now_add=True)
    contador = models.PositiveIntegerField(default=0)

    enlaces = EnlaceQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'Enlaces'

    def __str__(self):
        return f"URL: {self.url} Codigo: {self.codigo}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.codigo:
            self.codigo = Hashids(min_length=4, alphabet='abcdefghijklmnoqrstuvwxyz').encode(self.pk)
            self.save()

    def get_absolute_url(self):
        return reverse('core:detalle', kwargs=('pk', self.pk))