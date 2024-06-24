from django.shortcuts import render
from django.http import JsonResponse
from .models import ModbusConfig, Signal, SignalState
from modbus_communication import data_bank, int_to_bit, bit_to_int, received_bits, written_bits, set_updated_bits_callback

def index(request):
    global received_bits, written_bits
    config = ModbusConfig.objects.first()
    signals = Signal.objects.all()
    input_signals = signals.filter(direction='in')
    output_signals = signals.filter(direction='out')
    return render(request, 'modbus_app/index.html', {
        'config': config,
        'input_signals': input_signals,
        'output_signals': output_signals,
        'received_bits': received_bits,
        'written_bits': written_bits
    })

def update_signals(request):
    global received_bits
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'received_bits': received_bits})
    return JsonResponse({'status': 'failed'})

def send_signal(request):
    global written_bits
    if request.method == 'POST':
        signals = Signal.objects.filter(direction='in')
        bits = [0] * 16  # Initialize 16-bit array

        for signal in signals:
            signal_value = request.POST.get(signal.name) == 'true'
            if 'Prog' in signal.name:
                signal.program_number = int(request.POST.get(f'{signal.name}_program_number', 0))
            signal.save()
            bits[16 - signal.port] = int(signal_value)  # Map the signal to the correct bit position

        written_bits = "".join(map(str, bits))
        values = bit_to_int(bits)
        data_bank.set_holding_registers(0, [values])

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def update_received_bits(bits):
    global received_bits
    received_bits = bits

set_updated_bits_callback(update_received_bits)
