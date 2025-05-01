import argparse
import os
import fcntl
from enum import IntEnum
from pathlib import Path
import time
from stat import S_IWOTH
import ctypes
import logging

logger = logging.getLogger(__name__)


class PciPerformance(IntEnum):
    """Performance levels for PCI Edge TPU"""

    LOW = 0x0  # 62.5MHz
    MEDIUM = 0x1  # 125MHz
    HIGH = 0x2  # 250MHz
    MAX = 0x3  # 500MHz


APEX_IOCTL_PERFORMANCE_EXPECTATION = 0x40047F01
sys_device_path = Path("/sys/class/apex/apex_0/")
POLL_INTERVAL_PATH = sys_device_path / "temp_poll_interval"


# Performance level과 주파수 매핑
PERF_FREQ_MAP = {
    PciPerformance.MAX: 500.0,
    PciPerformance.HIGH: 250.0,
    PciPerformance.MEDIUM: 125.0,
    PciPerformance.LOW: 62.5,
}


class ApexPerformanceExpectationIoctl(ctypes.Structure):
    _fields_ = [("performance", ctypes.c_uint32)]


class PciDfsManager:
    """DFS Manager implementation for PCI Edge TPU devices."""

    def __init__(self, device_path="/dev/apex_0"):
        self._device_path = device_path
        self._fd = None

        self._check_tpu_writable()
        # DFS 완전 비활성화
        self._disable_dfs()

    @staticmethod
    def _check_tpu_writable():
        """Check if TPU trip points are writable."""
        if not POLL_INTERVAL_PATH.is_file():
            raise FileNotFoundError(f"{POLL_INTERVAL_PATH} does not exist.")
        file_stat = POLL_INTERVAL_PATH.stat()
        if not (file_stat.st_mode & S_IWOTH):
            raise PermissionError(f"{POLL_INTERVAL_PATH} is not writable by others.")

    @staticmethod
    def _disable_dfs():
        """Disable DFS."""
        with open(POLL_INTERVAL_PATH, "w") as f:
            f.write("0")

    @staticmethod
    def _read_value(path: Path) -> str:
        """Read value from a file."""
        with open(path, "r") as f:
            return f.read().strip()

    @staticmethod
    def _write_values(path, value):
        """Write value to a file."""
        with open(path, "w") as f:
            f.write(str(value))

    def open(self):
        if self._fd is None:
            self._fd = os.open(self._device_path, os.O_RDWR)
            return True
        return True

    def close(self):
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None

    def set_performance(self, performance_level: PciPerformance):
        """Set the performance level of the Edge TPU using both IOCTL and trip points.

        Args:
            performance_level: PciPerformance enum value

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.open():
            return False

        success = True

        # 2. IOCTL을 통한 성능 설정
        ioctl_buffer = ApexPerformanceExpectationIoctl()
        ctypes.memset(ctypes.byref(ioctl_buffer), 0, ctypes.sizeof(ioctl_buffer))
        ioctl_buffer.performance = performance_level.value

        ret = fcntl.ioctl(self._fd, APEX_IOCTL_PERFORMANCE_EXPECTATION, ioctl_buffer)
        if ret != 0:
            logger.error(f"Failed to set performance via IOCTL, return: {ret}")
            success = False

        return success

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--frequency", type=float, default=500.0)
    args = parser.parse_args()

    with PciDfsManager() as dfs_manager:
        if args.frequency == 500.0:
            logger.debug("\nTesting MAX performance:")
            dfs_manager.set_performance(PciPerformance.MAX)
            time.sleep(1)

        elif args.frequency == 250.0:
            logger.debug("\nTesting HIGH performance:")
            dfs_manager.set_performance(PciPerformance.HIGH)
            time.sleep(1)

        elif args.frequency == 125.0:
            logger.debug("\nTesting MEDIUM performance:")
            dfs_manager.set_performance(PciPerformance.MEDIUM)
            time.sleep(1)

        elif args.frequency == 62.5:
            logger.debug("\nTesting LOW performance:")
            dfs_manager.set_performance(PciPerformance.LOW)
            time.sleep(1)
