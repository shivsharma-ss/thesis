from django.db import models

# Create your models here.

class ModbusConfig(models.Model):
    ip_address = models.CharField(max_length=15, default='192.168.88.254')
    port = models.IntegerField(default=502)

class SignalState(models.Model):
    enable = models.BooleanField(default=False)
    clockwise = models.BooleanField(default=False)
    counter_clockwise = models.BooleanField(default=False)
    ready = models.BooleanField(default=False)
    ok = models.BooleanField(default=False)
    nok = models.BooleanField(default=False)
    in_cycle = models.BooleanField(default=False)
    cycle_complete = models.BooleanField(default=False)
    program_number = models.IntegerField(default=0)