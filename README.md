# LYWSD03MMC

Tools and scripts for working with Xiaomi LYWSD03MMC Bluetooth temperature and humidity sensors running ATC1441 custom firmware.

## Overview

This repository contains Python scripts for scanning and reading data from LYWSD03MMC sensors via Bluetooth Low Energy (BLE), as well as utilities for extracting authentication tokens from the Xiaomi Mi Home ecosystem.

## Features

- Scan for BLE advertisements from LYWSD03MMC sensors
- Parse ATC1441 custom firmware payload format
- Extract temperature, humidity, battery level, and voltage readings
- Retrieve Mi authentication tokens for device activation
- Verbose BLE advertisement inspection

## Scripts

### scan_atc.py

Scans for and parses BLE advertisements from LYWSD03MMC sensors running ATC1441 custom firmware.

**Features:**
- Automatically decodes ATC1441 payload format
- Displays temperature (°C), humidity (%), battery percentage and voltage
- Filter by known MAC addresses
- Real-time monitoring with timestamps
- RSSI signal strength indication

**Payload Format:**
```
Bytes 0-5:   MAC address
Bytes 6-7:   Temperature (int16 BE, divide by 10 for °C)
Byte 8:      Humidity (%)
Byte 9:      Battery percentage
Bytes 10-11: Battery voltage (mV, uint16 BE)
Byte 12:     Packet counter
```

**Usage:**
```bash
python3 scan_atc.py
```

**Configuration:**
Edit the `KNOWN_SENSORS` dictionary to filter specific devices:
```python
KNOWN_SENSORS = {
    "A4:C1:38:E2:3C:8B": "Living Room",
}
```

### scan_raw.py

Verbose BLE scanner that displays raw advertisement data from all nearby BLE devices.

**Features:**
- Shows device address and name
- Displays RSSI signal strength
- Lists all service UUIDs
- Dumps raw service data and manufacturer data
- Useful for debugging and analyzing BLE advertisement structure

**Usage:**
```bash
python3 scan_raw.py
```

### token_extractor/

Python tool for extracting Mi authentication tokens from Xiaomi Mi Home accounts. Required for activating LYWSD03MMC devices or accessing advanced features.

**Features:**
- Interactive and non-interactive modes
- Multi-region server support (CN, DE, US, RU, TW, SG, IN, I2)
- Encrypted API communication with Xiaomi cloud
- Device and home information retrieval
- Beacon key extraction for BLE devices

**Usage:**

Interactive mode:
```bash
cd token_extractor
python3 token_extractor.py
```

Non-interactive mode:
```bash
python3 token_extractor.py -ni -u USERNAME -p PASSWORD -s SERVER
```

**Options:**
- `-ni, --non_interactive`: Run without prompts
- `-u, --username`: Xiaomi account username
- `-p, --password`: Xiaomi account password
- `-s, --server`: Server region (cn, de, us, ru, tw, sg, in, i2)
- `-l, --log_level`: Logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `-o, --output`: Output file for results

**Dependencies:**
```bash
pip install -r token_extractor/requirements.txt
```

## Requirements

### Python Dependencies

For BLE scanning scripts:
```bash
pip install bleak
```

For token extractor:
```bash
pip install -r token_extractor/requirements.txt
```

Main dependencies:
- bleak - Bluetooth Low Energy platform-agnostic client
- requests - HTTP library for API calls
- pycryptodome - Cryptographic operations
- Pillow - Image processing
- colorama - Terminal color output

### System Requirements

- Python 3.7+
- Bluetooth Low Energy (BLE) adapter
- macOS, Linux, or Windows with BLE support

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd LYWSD03MMC
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install bleak
pip install -r token_extractor/requirements.txt
```

## Device Firmware

These scripts are designed to work with LYWSD03MMC sensors running the ATC1441 custom firmware. The custom firmware broadcasts temperature and humidity data in BLE advertisements, eliminating the need to connect to the device.

**ATC1441 Custom Firmware:**
- GitHub: https://github.com/atc1441/ATC_MiThermometer
- Provides enhanced BLE advertising format
- Improved battery life
- Better compatibility with open-source tools

## Troubleshooting

### Bluetooth Permissions

On macOS, you may need to grant Bluetooth permissions to your terminal application in System Preferences > Security & Privacy > Bluetooth.

### No Devices Found

- Ensure the sensor is within range (typically 10-30 meters)
- Verify the sensor battery is not depleted
- Check that Bluetooth is enabled on your computer
- Try running with `sudo` on Linux if permission issues occur

### Token Extraction Fails

- Verify your Xiaomi account credentials are correct
- Ensure you're using the correct server region
- Check that the device is registered in your Mi Home app
- Some regions may have different API requirements

## License

This project is provided as-is for educational and personal use.

## Contributing

Contributions are welcome. Please ensure code follows existing style and includes appropriate documentation.

## References

- ATC1441 Custom Firmware: https://github.com/atc1441/ATC_MiThermometer
- Telink Flasher: https://atc1441.github.io/TelinkFlasher.html
- Bleak BLE Library: https://github.com/hbldh/bleak
