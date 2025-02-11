import time
import serial

arduino = serial.Serial(port= '/dev/tty.usbmodem1301', baudrate=9600, timeout=0.1)
while True:
    output = f"0110001"
    arduino.write((output + "\n").encode())