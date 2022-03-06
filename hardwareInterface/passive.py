import asyncio
from datetime import datetime
from http import client
import json
import sys
import struct

from bleak import BleakScanner, BleakClient
import requests

CHARACTERISTIC_UUID = "f4a67d7d-379d-4183-9c03-4b6ea5103291"


def handle_data(sender, data):
    dateTimeObj = datetime.now().timestamp()
    no_elements, = struct.unpack('b', data[:1])
    data = data[1:]
    for i in range(no_elements):
        node_ID, = struct.unpack('<H', data[:2])
        data = data[2:]
        X, Y, Z, quality = struct.unpack('<iiib', data[:13])
        data = data[13:]
        print(X, Y, Z, dateTimeObj, hex(node_ID), quality)
        pload = {
            'x': str(X/1000),
            'y': str(Y/1000),
            'z': str(Z/1000),
            't': str(dateTimeObj),
            'hardwareId': str(hex(node_ID)),
            'quality': str(quality)
        }
        r = requests.post('http://127.0.0.1:8000/submit/',
                          data=json.dumps(pload))
        print(r)
        print(r.text)


def get_device_info(byte_data):
    node_id = struct.unpack('<Q', byte_data[:8])
    return hex(node_id[0])


def notification_handler(sender, data):  # For debugging purposes only
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))


async def main(wanted_name):
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and d.name.lower() == wanted_name.lower()
    )
    print("Device:")
    print(device)
    async with BleakClient(device.address) as client:
        device_info = await client.read_gatt_char("1e63b1eb-d4ed-444e-af54-c1e965192501")
        print("Node id: {0}".format(get_device_info(device_info)))
        await client.start_notify(CHARACTERISTIC_UUID, handle_data)
        await asyncio.sleep(10000.0)
        await client.stop_notify(CHARACTERISTIC_UUID)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} name")
        sys.exit(1)

    asyncio.run(main(sys.argv[1]))
