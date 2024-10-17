import serial
import time

# Configure the serial port
SERIAL_PORT = 'COM3'  # Change to your correct serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
BAUD_RATE = 115200  # Adjust if needed

def send_uart_data(serial_conn, data):
    """Send a list of 8-bit chunks over UART."""
    for byte in data:
        serial_conn.write(byte.to_bytes(1, byteorder='big'))
        time.sleep(0.01)  # Optional delay to ensure proper transmission

def read_and_transmit():
    # Open serial connection
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"Connected to {SERIAL_PORT}")

        # Read 32-bit instructions from the file
        with open('riscv_instructions.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                # Convert 32-bit binary string to an integer
                instruction = int(line, 2)

                # Split the 32-bit instruction into 4 bytes (8 bits each)
                bytes_to_send = [
                    (instruction >> 24) & 0xFF,  # Most significant byte
                    (instruction >> 16) & 0xFF,
                    (instruction >> 8) & 0xFF,
                    instruction & 0xFF            # Least significant byte
                ]

                # Send the 8-bit chunks over UART
                send_uart_data(ser, bytes_to_send)

                # Print each byte in binary format
                binary_bytes = [f'{byte:08b}' for byte in bytes_to_send]
                print(f"Sent: {binary_bytes}")

if __name__ == '__main__':
    read_and_transmit()
