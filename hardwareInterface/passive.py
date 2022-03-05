import asyncio
from http import client
import json
import sys
import struct

from bleak import BleakScanner, BleakClient
from datetime import datetime
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
        pload = {'x': str(X), 'y': str(Y), 'z': str(Z), 't': str(dateTimeObj), 'deviceId': str(hex(node_ID)), 'quality': str(quality)}
        r = requests.post('http://127.0.0.1:8000/submit/', data = json.dumps(pload))
        print(r)


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
    device_info = None
    async with BleakClient(device.address) as client:
        # svcs = await client.get_services()
        # print("Services:")
        # for service in svcs:
        #     print(service)
        device_info = await client.read_gatt_char("1e63b1eb-d4ed-444e-af54-c1e965192501")

        await client.start_notify(CHARACTERISTIC_UUID, handle_data)
        await asyncio.sleep(2.0)
        await client.stop_notify(CHARACTERISTIC_UUID)
    print("Node id: {0}".format(get_device_info(device_info)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} name")
        sys.exit(1)

    asyncio.run(main(sys.argv[1]))
