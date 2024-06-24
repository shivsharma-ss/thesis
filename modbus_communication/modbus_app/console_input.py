from modbus_communication import data_bank, bit_to_int, set_updated_bits_callback

def user_input():
    while True:
        user_input_value = input("Enter up to 16 bits (e.g. 1010101010101010): ")
        if not all(bit in '01' for bit in user_input_value) or len(user_input_value) > 16:
            print("Invalid input. Please enter a valid 16-bit binary number.")
            continue
        bin_list = [int(bit) for bit in user_input_value.zfill(16)]
        value = bit_to_int(bin_list)
        data_bank.set_holding_registers(0, [value])
        print(f"{value} written to register 0.")
        print(f"{bin_list} written to register 0.")

def display_updated_bits(bits):
    print(f"Updated bits: {bits}")

if __name__ == "__main__":
    set_updated_bits_callback(display_updated_bits)
    user_input()
