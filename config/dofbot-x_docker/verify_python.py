import sys
try:
    import smbus
    import smbus2
    print("Python version:", sys.version)
    print("smbus is installed:", smbus is not None)
    print("smbus2 is installed:", smbus2 is not None)
    print("Verification successful!")
except ImportError as e:
    print("Missing package:", e)
    sys.exit(1)
except Exception as e:
    print("Unexpected error:", e)
    sys.exit(1)
