#!/usr/bin/env python3
"""
PyADS Connection Test Script for TwinCAT 2.11
This script automatically installs requirements and tests the ADS connection.
Can be run directly on Windows.
"""

import subprocess
import sys
import os


def install_requirements():
    """Install required packages from requirements.txt"""
    print("=" * 60)
    print("Checking and installing requirements...")
    print("=" * 60)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(script_dir, "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print(f"ERROR: requirements.txt not found at {requirements_file}")
        return False
    
    try:
        # Install requirements using pip
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ])
        print("\nRequirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Failed to install requirements: {e}")
        return False


def test_pyads_import():
    """Test if pyads can be imported"""
    try:
        # Force reload in case it was just installed
        import importlib
        if 'pyads' in sys.modules:
            import pyads
            importlib.reload(pyads)
        else:
            import pyads
        print(f"✓ PyADS version {pyads.__version__} is installed")
        return True
    except ImportError:
        print("✗ PyADS is not installed")
        return False


def test_ads_connection():
    """Test connection to TwinCAT PLC"""
    print("\n" + "=" * 60)
    print("Testing ADS Connection to TwinCAT 2.11")
    print("=" * 60)
    
    try:
        import pyads
        import signal
        
        # Connection parameters
        # Note: ADS-IP format should be like "192.168.165.11" (assuming .1.1 was a typo)
        # If the actual ADS-IP is different, please modify accordingly
        ADS_NET_ID = "192.168.165.1.1.1"  # TwinCAT ADS Net ID (format: x.x.x.x.x.x)
        PLC_IP = "192.168.16.229"  # PLC IP address
        ADS_PORT = 801  # ADS port for TwinCAT 2.11
        
        print(f"\nConnection Parameters:")
        print(f"  ADS Net ID: {ADS_NET_ID}")
        print(f"  PLC IP:     {PLC_IP}")
        print(f"  ADS Port:   {ADS_PORT}")
        print(f"\nAttempting to connect (timeout: 10 seconds)...")
        
        # Create PLC connection
        plc = pyads.Connection(ADS_NET_ID, ADS_PORT, PLC_IP)
        
        # Define timeout handler (for non-Windows systems)
        def timeout_handler(signum, frame):
            raise TimeoutError("Connection attempt timed out")
        
        # Try to open connection with timeout
        try:
            # Set timeout for Unix-like systems
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
            
            plc.open()
            
            # Cancel alarm if set
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
                
            print("✓ Connection opened successfully!")
        except TimeoutError:
            print("✗ Connection timed out after 10 seconds")
            raise
        
        # Try to read device info
        try:
            device_name = plc.read_device_info()
            print(f"✓ Device Info: {device_name}")
        except Exception as e:
            print(f"⚠ Could not read device info: {e}")
        
        # Try to get PLC state
        try:
            state = plc.read_state()
            print(f"✓ PLC State: {state}")
        except Exception as e:
            print(f"⚠ Could not read PLC state: {e}")
        
        # Close connection
        plc.close()
        print("✓ Connection closed successfully!")
        
        print("\n" + "=" * 60)
        print("CONNECTION TEST PASSED!")
        print("=" * 60)
        return True
        
    except ImportError as e:
        print(f"\n✗ ERROR: PyADS not available: {e}")
        print("Please ensure requirements are installed correctly.")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: Connection failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Verify TwinCAT is running on the target PLC")
        print("  2. Check that the ADS Net ID is correct")
        print("  3. Ensure the PLC IP address is reachable")
        print("  4. Verify Windows Firewall allows ADS communication")
        print("  5. Check ADS route is configured on the PLC")
        print("\n" + "=" * 60)
        print("CONNECTION TEST FAILED!")
        print("=" * 60)
        return False


def main():
    """Main function to run the test"""
    print("\n" + "=" * 60)
    print("PyADS Connection Test Tool")
    print("For TwinCAT 2.11 Server")
    print("=" * 60 + "\n")
    
    # Step 1: Check if pyads is installed
    if not test_pyads_import():
        print("\nPyADS not found. Installing requirements...")
        if not install_requirements():
            print("\n✗ Failed to install requirements. Exiting.")
            sys.exit(1)
        
        # Verify installation
        if not test_pyads_import():
            print("\n✗ PyADS still not available after installation. Exiting.")
            sys.exit(1)
    
    # Step 2: Test the connection
    success = test_ads_connection()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
