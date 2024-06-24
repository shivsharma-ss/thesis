from django.db import models
import json
import os

# Import the JSON file path from webjsondatagetter.py
from webjsondatagetter import DEFAULT_FILE_PATH as JSON_FILE_PATH

# Load signals from JSON file
with open(JSON_FILE_PATH) as f:
    modules_data = json.load(f)
    IN_SIGNALS = [(entry['signal'], entry['port']) for entry in modules_data if entry['direction'] == 'in']
    OUT_SIGNALS = [(entry['signal'], entry['port']) for entry in modules_data if entry['direction'] == 'out']

class ModbusConfig(models.Model):
    ip_address = models.CharField(max_length=15, default='192.168.88.253')
    port = models.IntegerField(default=502)

class Signal(models.Model):
    name = models.CharField(max_length=50)
    direction = models.CharField(max_length=3, choices=[('in', 'Input'), ('out', 'Output')])
    port = models.IntegerField(default=0)  # Port corresponds to the position of the bit
    state = models.BooleanField(default=False)
    program_number = models.IntegerField(default=0, null=True, blank=True)  # For Prog and ProgAck signals

    def __str__(self):
        return self.name

def create_signal_states():
    fields = {
        'program_number': models.IntegerField(default=0),
        'program_acknowledge': models.IntegerField(default=0)
    }
    for signal, port in IN_SIGNALS + OUT_SIGNALS:
        fields[signal] = models.BooleanField(default=False)
    return type('SignalState', (models.Model,), fields)

SignalState = create_signal_states()
