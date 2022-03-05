import asyncio
from sqlite3 import Time
import sys

from bleak import discover, BleakClient
from asyncio.exceptions import TimeoutError


async def main():
    devices = await discover()
    service = "680c21d9-c946-4c1f-9c11-baa1c21329e7"
    characteristic = "f0f26c9b-2c8c-49ac-ab60-fe03def1b40c" # An anchor-specific characteristic corresponding to the persisted position

    print(devices[:2])


    for device in devices[:2]:
        client = None
        try:
            async with BleakClient(device.address) as client:
                services = await client.get_services()
                # if service in services:
                #     print(device)
                print("Services:")
                for service in services:
                    print(service)
                client.disconnect()
        except TimeoutError:
            client.disconnect()
            continue

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(f"Usage: <no arguments>")
        sys.exit(1)

    asyncio.run(main())