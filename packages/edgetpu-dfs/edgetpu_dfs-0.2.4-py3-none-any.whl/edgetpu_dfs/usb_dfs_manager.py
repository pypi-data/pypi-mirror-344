# Copyright 2024
# Licensed under the Apache License, Version 2.0

import usb.core
import usb.util
from dfs_interface import DfsManager

# USB Edge TPU device identifiers
USB_VENDOR_ID = 0x18D1
USB_PRODUCT_ID = 0x9302

# Register addresses
REG_ADDR_STATUS = 0xA0DC
REG_ADDR_CONTROL = 0xA318
REG_ADDR_INFO = 0xA0D8


class UsbDfsManager(DfsManager):
    """DFS Manager implementation for USB Edge TPU devices."""

    # Frequency data for different levels
    # Format: [0x5c, 0x02, 0x85, value]
    FREQ_DATA = {
        500.0: [0x5C, 0x02, 0x85, 0x00],
        250.0: [0x5C, 0x02, 0x85, 0x50],
        125.0: [0x5C, 0x02, 0x85, 0x60],
        62.5: [0x5C, 0x02, 0x85, 0xF0],
    }

    def __init__(self):
        """Initialize the USB DFS Manager by finding the device."""
        self.device = self._find_device()
        if not self.device:
            print("Warning: USB Edge TPU device not found")

    @staticmethod
    def detect_device():
        """Check if a USB Edge TPU device is available.

        Returns:
            bool: True if a USB Edge TPU device is found, False otherwise
        """
        dev = usb.core.find(idVendor=USB_VENDOR_ID, idProduct=USB_PRODUCT_ID)
        return dev is not None

    def _find_device(self):
        """Find and return the USB Edge TPU device.

        Returns:
            usb.core.Device or None: The USB device if found, None otherwise
        """
        return usb.core.find(idVendor=USB_VENDOR_ID, idProduct=USB_PRODUCT_ID)

    def is_device_available(self):
        """Check if the Edge TPU device is available.

        Returns:
            bool: True if the device is available, False otherwise
        """
        return self.device is not None

    def set_frequency(self, frequency: float):
        """Set the frequency of the Edge TPU to the specified level.

        Args:
            frequency: The desired frequency

        Returns:
            bool: True if the frequency was successfully set, False otherwise
        """
        if not self.is_device_available():
            return False

        try:
            # USB control transfer parameters
            bm_request_type = 0x40  # Host to device, vendor-specific
            b_request = 0x01
            w_value = REG_ADDR_CONTROL
            w_index = 0x01
            data = self.FREQ_DATA[frequency]
            timeout = 6000

            # Send the control transfer
            self.device.ctrl_transfer(bm_request_type, b_request, w_value, w_index, data, timeout)
            return True
        except Exception as e:
            print(f"Error setting frequency: {e}")
            return False

    def get_current_frequency(self):
        """Get the current frequency information of the Edge TPU.

        Returns:
            dict: A dictionary containing register values related to frequency
        """
        if not self.is_device_available():
            return {"error": "Device not available"}

        try:
            # Parameters for reading registers
            bm_request_type = 0xC0  # Device to host, vendor-specific
            b_request = 0x01
            w_index = 0x01
            length = 4
            timeout = 6000

            # Read status register (0xA0DC)
            status_data = self.device.ctrl_transfer(
                bm_request_type, b_request, REG_ADDR_STATUS, w_index, length, timeout
            )

            # Read info register (0xA0D8)
            info_data = self.device.ctrl_transfer(
                bm_request_type, b_request, REG_ADDR_INFO, w_index, length, timeout
            )

            return {
                "status_register": list(status_data),
                "info_register": list(info_data),
                "frequency": self._interpret_frequency(status_data),
            }
        except Exception as e:
            return {"error": f"Error reading frequency: {e}"}

    def _interpret_frequency(self, status_data):
        """Interpret the frequency from the status register data.

        This is a simplified interpretation and may need to be adjusted
        based on actual device behavior.

        Args:
            status_data: The data read from the status register

        Returns:
            float: The current frequency
        """
        # This is a placeholder implementation
        # Actual interpretation depends on the specific meaning of register values
        if len(status_data) < 4:
            return "Unknown"

        # This logic should be customized based on actual device behavior
        value = status_data[3]
        if value == 0x00:
            return 500.0
        elif value <= 0x50:
            return 250.0
        elif value <= 0x60:
            return 125.0
        else:
            return 62.5
