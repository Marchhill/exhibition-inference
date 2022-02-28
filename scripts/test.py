import asyncio
from http import client
import sys
import struct

from bleak import BleakScanner, BleakClient

CHARACTERISTIC_UUID = "003bbdf2-c634-4b3d-ab56-7ec889b89a37"

def handle_data(sender, data):
    data_mode, = struct.unpack('b',data[:1])
    data = data[1:]
    if data_mode in [0,2]:
        X,Y,Z,quality = struct.unpack('=iiib',data[:13])
        data = data[13:]
        print(X,Y,Z,quality)


    if data_mode in [1,2]:
        num_distances, = struct.unpack('b',data[:1])
        data = data[1:]
        for i in range(num_distances):
            if len(data)<7:
                data += b"\x00"*(7-len(data))
            node_id, distance, quality = struct.unpack('=2sib',data[:7])
            data = data[7:]
            print(node_id.hex(),distance,quality)

def notification_handler(sender, data):
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
        await asyncio.sleep(5.0)
        await client.stop_notify(CHARACTERISTIC_UUID)
    print(device_info)
            


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} name")
        sys.exit(1)

    asyncio.run(main(sys.argv[1]))