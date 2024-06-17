# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import ModbusConfig, SignalState
from pyModbusTCP.server import DataBank, ModbusServer
from threading import Thread
from time import sleep

# Initialize DataBank
data_bank = DataBank()

def int_to_bit(value):
    bin_str = format(value, '016b')
    return [int(bit) for bit in bin_str]

def bit_to_int(bin_list):
    bin_str = ''.join(str(bit) for bit in bin_list)
    return int(bin_str, 2)

received_bits = ""
written_bits = ""

def modbus_server():
    global received_bits
    config = ModbusConfig.objects.first()
    ip_address = '192.168.88.254'  # Bind to specific IP
    port = config.port if config else 502
    server = ModbusServer(ip_address, port, no_block=True, data_bank=data_bank)
    try:
        server.start()
        while True:
            current_state = data_bank.get_holding_registers(2048, 1)
            if current_state:
                bin_list = int_to_bit(current_state[0])
                received_bits = "".join(map(str, bin_list))
                SignalState.objects.update_or_create(
                    id=1,
                    defaults={
                        'enable': bin_list[0],
                        'clockwise': bin_list[1],
                        'counter_clockwise': bin_list[2],
                        'ready': bin_list[3],
                        'ok': bin_list[4],
                        'nok': bin_list[5],
                        'in_cycle': bin_list[6],
                        'cycle_complete': bin_list[7],
                        'program_number': bit_to_int(bin_list[8:])
                    }
                )
            sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        server.stop()

modbus_thread = Thread(target=modbus_server)
modbus_thread.daemon = True
modbus_thread.start()

def index(request):
    global received_bits, written_bits
    config = ModbusConfig.objects.first()
    signals = SignalState.objects.first()
    if not config:
        config = ModbusConfig.objects.create(ip_address='192.168.88.254', port=502)
    if not signals:
        signals = SignalState.objects.create()
    return render(request, 'modbus_app/index.html', {'config': config, 'signals': signals, 'received_bits': received_bits, 'written_bits': written_bits})

def update_signals(request):
    global received_bits
    if request.method == 'POST':
        current_state = data_bank.get_holding_registers(2048, 1)
        if current_state:
            bin_list = int_to_bit(current_state[0])
            received_bits = "".join(map(str, bin_list))
            return JsonResponse({'status': 'success', 'received_bits': received_bits})
    return JsonResponse({'status': 'failed'})

def send_signal(request):
    global written_bits
    if request.method == 'POST':
        enable = request.POST.get('enable') == 'true'
        clockwise = request.POST.get('clockwise') == 'true'
        counter_clockwise = request.POST.get('counter_clockwise') == 'true'
        ready = request.POST.get('ready') == 'true'
        ok = request.POST.get('ok') == 'true'
        nok = request.POST.get('nok') == 'true'
        in_cycle = request.POST.get('in_cycle') == 'true'
        cycle_complete = request.POST.get('cycle_complete') == 'true'
        program_number = int(request.POST.get('program_number'))

        signals = SignalState.objects.first()
        signals.enable = enable
        signals.clockwise = clockwise
        signals.counter_clockwise = counter_clockwise
        signals.ready = ready
        signals.ok = ok
        signals.nok = nok
        signals.in_cycle = in_cycle
        signals.cycle_complete = cycle_complete
        signals.program_number = program_number
        signals.save()

        bits = [
            int(enable), int(clockwise), int(counter_clockwise),
            int(ready), int(ok), int(nok), int(in_cycle),
            int(cycle_complete)
        ]
        program_bits = list(map(int, format(program_number, '08b')))
        full_bits = bits + program_bits

        bit_list = [int(bit) for bit in full_bits]

        written_bits = "".join(map(str, full_bits))
        values = bit_to_int(bit_list)  
        data_bank.set_holding_registers(0, [values])

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})
