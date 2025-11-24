import asyncio
import struct
from datetime import datetime

from bleak import BleakScanner

SERVICE_UUID_181A = "0000181a-0000-1000-8000-00805f9b34fb"

KNOWN_SENSORS = {
    # optional: real MAC from Telink UI if you want to filter later
    "A4:C1:38:E2:3C:8B": "Computer Room",
    "A4:C1:38:E9:04:00": "Living Room",
}

def parse_atc_payload(data: bytes):
    """
    ATC1441 payload (this firmware build uses BIG-endian for temp & voltage):

        0-5   : MAC address
        6-7   : temperature (int16 BE, value / 10 = °C)
        8     : humidity (%)
        9     : battery (%)
        10-11 : battery voltage (mV, uint16 BE)
        12    : packet counter
    """
    if len(data) < 13:
        return None

    mac_bytes = data[0:6]
    mac = ":".join(f"{b:02X}" for b in mac_bytes)

    # NOTE: big-endian here
    temp_raw = int.from_bytes(data[6:8], byteorder="big", signed=True)
    humidity = data[8]
    battery_pct = data[9]
    batt_mv = int.from_bytes(data[10:12], byteorder="big", signed=False)
    packet_counter = data[12]

    temp_c = temp_raw / 10.0

    return {
        "mac": mac,
        "temperature_c": temp_c,
        "humidity_pct": humidity,
        "battery_pct": battery_pct,
        "battery_mv": batt_mv,
        "packet_counter": packet_counter,
    }

async def main():
    print("Scanning for ATC sensors (Ctrl+C to stop)...")

    def callback(device, advertisement_data):
        service_data = advertisement_data.service_data.get(SERVICE_UUID_181A)
        if not service_data:
            return

        raw = bytes(service_data)

        parsed = parse_atc_payload(raw)
        if not parsed:
            return

        mac = parsed["mac"]

        if KNOWN_SENSORS and mac not in KNOWN_SENSORS:
            return

        label = KNOWN_SENSORS.get(mac, device.name or mac)
        rssi = getattr(advertisement_data, "rssi", None)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(
            f"[{now}] {label} ({mac}, RSSI={rssi}) -> "
            f"{parsed['temperature_c']:.1f} °C, "
            f"{parsed['humidity_pct']} % RH, "
            f"battery {parsed['battery_pct']}% ({parsed['battery_mv']} mV, "
            f"ctr={parsed['packet_counter']})"
        )

    scanner = BleakScanner(callback)
    await scanner.start()

    try:
        while True:
            await asyncio.sleep(10)
    finally:
        await scanner.stop()

if __name__ == "__main__":
    asyncio.run(main())