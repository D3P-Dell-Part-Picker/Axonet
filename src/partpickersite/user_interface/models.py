from django.db import models


class Racks(models.Model):
    part_number = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=20)
    ip = models.CharField(max_length=20)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'racks'


# TODO setup model for colors and part locations
"\""


class LEDS(models.Model):
    location = models.CharField(max_length=30)
    color = models.CharField(max_length=255)
    session_keys = models.TextField(blank=True)
    timeout = models.DateTimeField(blank=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'leds'


"\""
