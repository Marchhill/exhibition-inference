import asyncio
from http import client
import sys
import struct

from bleak import BleakScanner, BleakClient, BleakError

from test import get_device_info

CHARACTERISTIC_UUID = "1e63b1eb-d4ed-444e-af54-c1e965192501"

async def get_ID(name):
    device = None

    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and d.name.lower() == name.lower()
    )            

    device_info = None

    if (device == None):
        print("Could not find {0}".format(name))
        return None

    async with BleakClient(device.address) as client:
        device_info = await client.read_gatt_char(CHARACTERISTIC_UUID)
        await client.disconnect()
    
    device_ID = get_device_info(device_info)
    shortened_device_ID = device_ID.strip()[-4:]

    print("{0} has ID {1}, shortened to {2}".format(device, device_ID, shortened_device_ID))
    
    return (device_ID, shortened_device_ID)

async def get_IDs(names):
    result = {}

    for name in names:
        result[name] = await get_ID(name)

    return result

async def main(names):
    print(await get_IDs(names))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <list of tags and anchors>")
        sys.exit(1)

    asyncio.run(main(sys.argv[1:]))