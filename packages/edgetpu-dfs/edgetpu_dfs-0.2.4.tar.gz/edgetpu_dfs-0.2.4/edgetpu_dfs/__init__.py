"""EdgeTPU DFS (Dynamic Frequency Scaling) utilities.

This package provides tools to manage Dynamic Frequency Scaling on Edge TPU devices.
"""

from .pci_dfs_manager import PciDfsManager
from .pci_dfs_manager_with_trip_point import PciDfsManagerWithTripPoint
from .usb_dfs_manager import UsbDfsManager
from .dfs_interface import DfsInterface
from .dfs_utils import get_device_type

__all__ = [
    "PciDfsManager",
    "PciDfsManagerWithTripPoint",
    "UsbDfsManager",
    "DfsInterface",
    "get_device_type",
]
