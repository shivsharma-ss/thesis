from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .models import ModbusConfig, Signal, SignalState
from .modbus_communication import data_bank, int_to_bit, bit_to_int, received_bits, written_bits, set_updated_bits_callback
import logging

@ensure_csrf_cookie
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

@ensure_csrf_cookie
def api_data(request):
    input_signals = Signal.objects.filter(direction='in')
    output_signals = Signal.objects.filter(direction='out')

    input_signals_list = [signal.to_dict() for signal in input_signals]
    output_signals_list = [signal.to_dict() for signal in output_signals]

    data = {
        "input_signals": input_signals_list,
        "output_signals": output_signals_list,
    }
    return JsonResponse(data)

@csrf_exempt
def update_signals(request):
    output_signals = Signal.objects.filter(direction='out')
    received_bits = ''.join(['1' if signal.state else '0' for signal in output_signals])
    logging.info(f'Output signals updated. Received bits: {received_bits}')
    return JsonResponse({'status': 'success', 'received_bits': received_bits})

@csrf_exempt
def send_signal(request):
    global written_bits
    if request.method == 'POST':
        signals = Signal.objects.filter(direction='in')
        bits = [0] * 16
        for signal in signals:
            signal_value = request.POST.get(signal.name) == 'true'
            if 'Prog' in signal.name:
                signal.program_number = int(request.POST.get(f'{signal.name}_program_number', 0))
            bits[16 - signal.port] = int(signal_value)
            signal.state = bits[16 - signal.port]
            signal.save()
        written_bits = "".join(map(str, bits))
        values = bit_to_int(bits)
        data_bank.set_holding_registers(0, [values])
        logging.info(f'Signal sent successfully. Written bits: {written_bits}')
        return JsonResponse({'status': 'success'})
    logging.info('Failed to send signal. Request method was not POST.')
    return JsonResponse({'status': 'failed'})

def update_received_bits(bits):
    global received_bits
    received_bits = bits

    bits = list(map(int, received_bits))
    signals = Signal.objects.filter(direction='out')
    for signal in signals:
        signal.state = bits[16 - signal.port]
        signal.save()
    logging.info('Received bits updated successfully.')

@csrf_exempt
def update_state(request):
    if request.method == 'POST':
        signals = Signal.objects.filter(direction='in')
        bits = [0] * 16
        for signal in signals:
            signal_value = request.POST.get(signal.name) == 'true'
            if 'Prog' in signal.name:
                signal.program_number = int(request.POST.get(f'{signal.name}_program_number', 0))
            bits[16 - signal.port] = int(signal_value)
            signal.state = bits[16 - signal.port]
            signal.save()
        logging.info('State updated successfully.')
        return JsonResponse({'status': 'success'})
    logging.info('Failed to update state. Request method was not POST.')
    return JsonResponse({'status': 'failed'})

set_updated_bits_callback(update_received_bits)
