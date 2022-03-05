from usb_util import usb_connect, usb_send_command
import time


def send_command(ser, cmd, args):
    ser.read_all()
    usb_send_command(ser, cmd + " " + args)

    ser.readline()
    assert ser.readline() == cmd.encode() + \
        b": ok\r\n", "device error, restart and try again"


ser = usb_connect()

while True:
    ser.read_all()
    usb_send_command(ser, "si")
    time.sleep(0.5)
    info = [x.decode() for x in ser.read_all().split(b"\r\n")]

    name = "Not set"
    mode = "Not set"

    for info_line in info:
        if "cfg:" in info_line:
            name = info_line.split("=")[-1]
        if "mode:" in info_line:
            raw_mode = info_line.split(": ")[-1]

            if raw_mode in ["ani (act,-)", "ani (act,real)"]:
                mode = "Anchor"
            if raw_mode == "tn (act,twr,np,le)":
                mode = "Tag"
            if raw_mode == "an (pasv,-)":
                mode = "Listener"

    if name == "Not set":
        print("Device error, restart and try again")
        exit()

    print("Device label:", name)
    print("Device mode:", mode)
    reconf = input("Reconfigure device? (Y/n) ").upper()
    if reconf == "N":
        break
    print("Device types:")
    print(" [A] Anchor")
    print(" [T] Tag")
    print(" [L] Listener")
    device_type = input("Configure device as (A/T/L): ").upper()

    device_name = input("New device label [press enter to not update]: ")

    if device_name != "":
        # Set device label
        print("Setting device label to", device_name)
        send_command(ser, "nls", device_name)

    print("Configuring network")
    send_command(ser, "nis", "0x0DDB")

    print("Setting update frequency")
    send_command(ser, "aurs", "10 10")

    if device_type == "A":
        # Set mode to anchor, and then reconnect
        print("Setting mode to Anchor")
        usb_send_command(ser, "nmi")
        time.sleep(1)
        ser.close()
        ser = usb_connect(silent=True)
        time.sleep(1)
        ser.read_all()

        # Configure anchor
        send_command(ser, "acas", "1 0 0 0 1 1 0")

        usb_send_command(ser, "apg")
        ser.readline()
        current_pos = " ".join(ser.readline().decode().split(" ")[1:-1])
        print("Set position (mm): ", current_pos)
        update_position = input("Update position of anchor? (y/N) ").upper()
        if update_position == "Y":
            X = input("Anchor position X (in mm): ")
            Y = input("Anchor position Y (in mm): ")
            Z = input("Anchor position Z (in mm): ")
            send_command(ser, "aps", "{} {} {}".format(X, Y, Z))

    elif device_type == "T":
        # Set mode to tag, and then reconnect
        print("Setting mode to Tag")
        usb_send_command(ser, "nmt")
        time.sleep(1)
        ser.close()
        ser = usb_connect(silent=True)
        time.sleep(1)
        ser.read_all()

        # Configure tag
        send_command(ser, "acts", "0 0 0 1 0 0 1 2 0")

    elif device_type == "L":
        # Set mode to anchor, and then reconnect
        usb_send_command(ser, "nma")
        time.sleep(1)
        ser.close()
        ser = usb_connect(silent=True)
        time.sleep(1)
        ser.read_all()

        # Set UWB mode to passive
        usb_send_command(ser, "nmp")
        time.sleep(1)
        ser.close()
        ser = usb_connect(silent=True)
        time.sleep(1)
        print("Set mode to listener")
        ser.read_all()

        send_command(ser, "acas", "1 0 0 0 1 2 0")
    else:
        print("Invalid option")
        continue
    break

# usb_send_command(ser,"reset")


ser.close()
ser = usb_connect(silent=True)
time.sleep(1)
ser.close()
print("Done!")
