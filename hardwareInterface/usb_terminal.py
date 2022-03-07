import time
from usb_util import usb_connect, usb_send_command

ser = usb_connect()
ser.write(b'si\r')
time.sleep(1)
print(ser.readall().decode())
while True:
    try:
        usb_send_command(ser, input())
        print(ser.readall().decode())
    except KeyboardInterrupt:
        ser.close()
        break
