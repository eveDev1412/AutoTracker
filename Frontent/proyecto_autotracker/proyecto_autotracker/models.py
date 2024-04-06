from django.db import models


class MiModelo(models.Model):

    id_traking = models.IntegerField()
    fecha_avistamiento = models.TimeField()
    ubicación = models.CharField(max_length=16)
    hora = models.DateField()
    estatus = models.IntegerField()
    notificaciones = models.IntegerField()