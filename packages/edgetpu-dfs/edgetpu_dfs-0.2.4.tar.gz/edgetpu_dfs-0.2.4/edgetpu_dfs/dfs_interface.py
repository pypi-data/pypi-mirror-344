# Copyright 2024
# Licensed under the Apache License, Version 2.0

from abc import ABC, abstractmethod


class DfsManager(ABC):
    """Interface for Dynamic Frequency Scaling managers for Edge TPU devices."""

    @abstractmethod
    def set_frequency(self, frequency: float) -> bool:
        """Set the frequency of the Edge TPU to the specified level.

        Args:
            frequency: The desired frequency

        Returns:
            bool: True if the frequency was successfully set, False otherwise
        """
        pass

    @abstractmethod
    def get_current_frequency(self) -> dict:
        """Get the current frequency information of the Edge TPU.

        Returns:
            dict: A dictionary containing current frequency information
        """
        pass

    @abstractmethod
    def is_device_available(self) -> bool:
        """Check if the Edge TPU device is available.

        Returns:
            bool: True if the device is available, False otherwise
        """
        pass


def create_dfs_manager(device_type: str = None):
    """Factory function to create appropriate DFS manager based on device type.

    Args:
        device_type: 'usb', 'pci', or None (auto-detect)

    Returns:
        DfsManager: An instance of the appropriate DFS manager
    """
    from usb_dfs_manager import UsbDfsManager
    from pci_dfs_manager import PciDfsManager

    if device_type == "usb" or (device_type is None and UsbDfsManager.detect_device()):
        return UsbDfsManager()
    elif device_type == "pci" or (device_type is None and PciDfsManager.detect_device()):
        return PciDfsManager()
    else:
        raise ValueError("No supported Edge TPU device found or specified device type is invalid")
