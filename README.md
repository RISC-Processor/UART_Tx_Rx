# UART Transmitter and Receiver
This project implements UART for Tx and Rx, a bytes module for serial communication in RTL and Python. 
The project also contains a dummy RegFile (32, 32-bit registers) that can be transmitted through UART Tx. 

## Features

Baudrate is set to 115200 which can be changed.

## Note

1. An external TTL converter is required.  
2. Use GPIO pins in FPGA for Tx and Rx pins.      

3. FPGA pushbuttons (Keys) used for reset and enable transmitting regFile.  
4. LEDs are for debugging purposes.      

**Python TX instructions       --> HDL Rx receive them   --> put them in dummy Imem.**

**Dummy regFile send reg vals  --> HDL Tx to send them   --> Python receiver grab them.**
