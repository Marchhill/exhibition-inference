import serial
import time
import serial.tools.list_ports


def usb_connect(silent=False):
    ports = serial.tools.list_ports.comports()

    if len(ports) == 0:
        print("No connected device")
        exit()

    port = ports[0][0]
    if not silent:
        print("Connecting to device on port", port)

    ser = serial.Serial()
    ser.port = port
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1
    ser.open()
    ser.write(b'\r\r')
    time.sleep(1)
    return ser


def usb_send_command(ser, data):
    data = data.encode() + b"\r"
    for i in range(0, len(data), 5):
        ser.write(data[i:i+5])
        time.sleep(0.2)
