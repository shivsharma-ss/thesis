from pyModbusTCP.server import DataBank, ModbusServer
from threading import Thread
from time import sleep

data_bank = DataBank()

def int_to_bit(value):
    bin_str = format(value, '016b')
    return [int(bit) for bit in bin_str]

def bit_to_int(bin_list):
    bin_str = ''.join(str(bit) for bit in bin_list)
    return int(bin_str, 2)

received_bits = ""
written_bits = ""
updated_bits_callback = None

def set_updated_bits_callback(callback):
    global updated_bits_callback
    updated_bits_callback = callback

def check_for_updates():
    global received_bits
    previous_state = None
    while True:
        current_state = data_bank.get_holding_registers(2048, 1)
        if current_state and current_state != previous_state:
            bin_list = int_to_bit(current_state[0])
            received_bits = "".join(map(str, bin_list))
            if updated_bits_callback:
                updated_bits_callback(received_bits)
            previous_state = current_state
        sleep(0.05)

def start_modbus_server():
    ip_address = '192.168.88.253'
    port = 502
    server = ModbusServer(ip_address, port, no_block=True, data_bank=data_bank)
    try:
        server.start()
        check_for_updates_thread = Thread(target=check_for_updates)
        check_for_updates_thread.daemon = True
        check_for_updates_thread.start()
        while True:
            sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        server.stop()

modbus_thread = Thread(target=start_modbus_server)
modbus_thread.daemon = True
modbus_thread.start()
