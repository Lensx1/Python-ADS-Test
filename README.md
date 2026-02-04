# Python-ADS-Test

A Python script to test PyADS connection to TwinCAT 2.11 PLC.

## Features

- Automatically installs required dependencies (PyADS)
- Tests connection to TwinCAT 2.11 server
- Provides detailed connection status and troubleshooting information
- Can be run directly on Windows

## Prerequisites

- Python 3.6 or higher installed on Windows
- Network connectivity to the TwinCAT PLC
- TwinCAT runtime running on the target PLC

## Usage

### Running the Script

Simply double-click `test_ads_connection.py` or run from command prompt:

```cmd
python test_ads_connection.py
```

The script will:
1. Check if PyADS is installed
2. Install it automatically if not present
3. Attempt to connect to the PLC
4. Display connection status and device information

### Configuration

Edit the connection parameters in `test_ads_connection.py` if needed:

```python
ADS_NET_ID = "192.168.165.1.1.1"  # TwinCAT ADS Net ID
PLC_IP = "192.168.16.229"         # PLC IP address
ADS_PORT = 801                     # ADS port for TwinCAT 2.11
```

## Troubleshooting

If the connection fails, check:

1. TwinCAT is running on the target PLC
2. The ADS Net ID is correct (format: x.x.x.x.x.x)
3. The PLC IP address is reachable (try `ping 192.168.16.229`)
4. Windows Firewall allows ADS communication (TCP/UDP port 48898)
5. ADS route is configured on the PLC to allow your PC to connect

## Files

- `test_ads_connection.py` - Main test script
- `requirements.txt` - Python package dependencies
