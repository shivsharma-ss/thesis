from django.db import models
from config import IN_SIGNALS, OUT_SIGNALS

class ModbusConfig(models.Model):
    ip_address = models.CharField(max_length=15, default='192.168.88.254')
    port = models.IntegerField(default=502)

class Signal(models.Model):
    name = models.CharField(max_length=50)
    direction = models.CharField(max_length=3, choices=[('in', 'Input'), ('out', 'Output')])
    port = models.IntegerField(default=0)  # Port corresponds to the position of the bit
    state = models.BooleanField(default=False)
    program_number = models.IntegerField(default=0, null=True, blank=True)  # For Prog and ProgAck signals

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'name': self.name,
            'direction': self.direction,
            'port': self.port,
            'state': self.state,
            'program_number': self.program_number,
        }

def create_signal_states():
    fields = {
        '__module__': __name__,
        'program_number': models.IntegerField(default=0),
        'program_acknowledge': models.IntegerField(default=0)
    }
    for signal, port in IN_SIGNALS + OUT_SIGNALS:
        fields[signal] = models.BooleanField(default=False)
    return type('SignalState', (models.Model,), fields)

SignalState = create_signal_states()
