import serial

# Configure the UART (Change COM port and baudrate as needed)
uart = serial.Serial('COM3', baudrate=115200, timeout=1)  # Replace 'COMx' with your actual COM port

# File names for different types of data
reg_file_name = 'register_file.txt'
data_mem_file_name = 'data_memory.txt'
instr_mem_file_name = 'instruction_memory.txt'

# Function to read a single 32-bit word from UART
def read_32bit_word():
    word = 0
    for i in range(4):  # Read 4 bytes to form one 32-bit value
        byte = uart.read()  # Read one byte from UART
        if byte:  # If byte is received
            word = (word << 8) | int.from_bytes(byte, 'big')  # Shift and accumulate bytes
    return word

# Function to read 32 words (for register file)
def read_register_file():
    data = []
    for _ in range(32):  # Read exactly 32, 32-bit words for register file
        data.append(read_32bit_word())
    return data

# Function to read infinite length memory until the next identifier is found
def read_memory():
    data = []
    while True:
        byte = uart.read()  # Peek at the next byte
        if not byte:
            break  # End of stream
        if byte[0] in (0x01, 0x02, 0x03):
            uart.putback(byte)  # Put back the byte to handle the next identifier
            break  # Stop reading memory when a new identifier is found
        else:
            data.append(read_32bit_word())
    return data

# Function to store data to a file
def store_data_to_file(file_name, data):
    with open(file_name, 'w') as file:
        for word in data:
            file.write(f'{word:032b}\n')  # Write each 32-bit word in binary format

# Main function to process the received data
def main():
    while True:
        print("Waiting for data identifier...")
        identifier = uart.read()  # Read the identifier byte

        if identifier:
            identifier = int.from_bytes(identifier, 'big')
            print(f"Received identifier: {identifier:08b}")

            # Determine the type of data based on the identifier
            if identifier == 0x01:
                print("Reading Register File data...")
                reg_data = read_register_file()
                print("Storing Register File data...")
                store_data_to_file(reg_file_name, reg_data)
                print(f"Data saved to {reg_file_name}")

            elif identifier == 0x02:
                print("Reading Data Memory...")
                data_mem_data = read_memory()
                print("Storing Data Memory...")
                store_data_to_file(data_mem_file_name, data_mem_data)
                print(f"Data saved to {data_mem_file_name}")

            elif identifier == 0x03:
                print("Reading Instruction Memory...")
                instr_mem_data = read_memory()
                print("Storing Instruction Memory...")
                store_data_to_file(instr_mem_file_name, instr_mem_data)
                print(f"Data saved to {instr_mem_file_name}")

            else:
                print("Unknown identifier received, skipping...")

if __name__ == '__main__':
    main()
