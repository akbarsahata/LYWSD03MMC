import asyncio
from bleak import BleakScanner

async def main():
    print("Verbose scan (Ctrl+C to stop)...")

    def callback(device, advertisement_data):
        print("----")
        print("Device:")
        print("  address:", device.address)   # random UUID on macOS – expected
        print("  name   :", device.name)
        print("Adv data:")
        print("  RSSI           :", getattr(advertisement_data, "rssi", None))
        print("  service_uuids  :", advertisement_data.service_uuids)
        print("  service_data   :", {
            k: bytes(v) for k, v in advertisement_data.service_data.items()
        })
        print("  manufacturer_data:", {
            k: bytes(v) for k, v in advertisement_data.manufacturer_data.items()
        })

    scanner = BleakScanner(callback)
    await scanner.start()

    try:
        while True:
            await asyncio.sleep(5)
    finally:
        await scanner.stop()

if __name__ == "__main__":
    asyncio.run(main())