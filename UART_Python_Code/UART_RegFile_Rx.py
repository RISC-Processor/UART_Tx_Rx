import serial
import time

# Configure the UART (serial port)
ser = serial.Serial('COM3', baudrate=115200, timeout=1)

# Open the serial port if not already open
if not ser.is_open:
    ser.open()

# Function to read 32-bit words (4 bytes) from UART and store them in a list
def read_uart():
    received_words = []  # List to store received 4-byte words

    try:
        while len(received_words) < 32:  # Continue until we have 32 words
            if ser.in_waiting >= 4:  # Check if there are at least 4 bytes waiting
                bytes_data = ser.read(4)  # Read 4 bytes from UART
                received_words.append(bytes_data)  # Add bytes to list

        # Print the list of 32 registers
        for i, word in enumerate(received_words):
            formatted_word = [f"{byte:08b}" for byte in word]
            print(f"R{i+1}: {formatted_word}")  # Print as R1, R2, ...

    except KeyboardInterrupt:
        # Close the serial port when interrupted
        print("Exiting program")
        ser.close()

if __name__ == "__main__":
    read_uart()
