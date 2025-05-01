from pathlib import Path
import time
from stat import S_IWOTH
import logging

logger = logging.getLogger(__name__)

sys_device_path = Path("/sys/class/apex/apex_0/")
TRIP_POINTS_PATHS = [sys_device_path / f"trip_point{i}_temp" for i in range(3)]
POLL_INTERVAL_PATH = sys_device_path / "temp_poll_interval"


# 주파수별 trip point 매핑
FREQ_TRIP_POINTS = {
    500.0: (92800, 93800, 94800),  # MAX
    250.0: (4800, 93800, 94800),  # HIGH
    125.0: (4800, 5800, 94800),  # MEDIUM
    62.5: (4800, 5800, 6800),  # LOW
}


class PciDfsManager:
    """DFS Manager implementation for PCI Edge TPU devices."""

    def __init__(self):
        self._check_tpu_writable()

    def set_performance(self, freq: float):
        """Set the performance level of the Edge TPU using both IOCTL and trip points.

        Args:
            freq: Frequency to set

        Returns:
            bool: True if successful, False otherwise
        """

        success = True

        # Trip points를 통한 성능 설정
        trip_points = FREQ_TRIP_POINTS[freq]

        try:
            changed = self._change_trip_points(*trip_points)
            if changed:
                logger.debug(f"Changed TPU frequency to {freq} MHz via trip points")
        except Exception as e:
            logger.error(f"Failed to set trip points: {e}")
            success = False

        return success

    @staticmethod
    def _check_tpu_writable():
        """Check if TPU trip points are writable."""
        for path in TRIP_POINTS_PATHS:
            if not path.is_file():
                raise FileNotFoundError(f"{path} does not exist.")
            file_stat = path.stat()
            if not (file_stat.st_mode & S_IWOTH):
                raise PermissionError(f"{path} is not writable by others.")

        if not POLL_INTERVAL_PATH.is_file():
            raise FileNotFoundError(f"{POLL_INTERVAL_PATH} does not exist.")
        file_stat = POLL_INTERVAL_PATH.stat()
        if not (file_stat.st_mode & S_IWOTH):
            raise PermissionError(f"{POLL_INTERVAL_PATH} is not writable by others.")

        with open(POLL_INTERVAL_PATH, "w") as f:
            f.write("10")

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

    @classmethod
    def _change_trip_points(cls, t1, t2, t3):
        """Change TPU trip points.

        Args:
            t1, t2, t3: Target temperature values for trip points

        Returns:
            bool: True if values were changed, False if no change was needed
        """
        target_values = [str(t1), str(t2), str(t3)]

        # 현재 값 확인
        current_values = [cls._read_value(path) for path in TRIP_POINTS_PATHS]

        # 현재 값이 목표값과 같으면 early return
        if current_values == target_values:
            logger.debug(f"Trip points already at target values: {target_values}")
            return False

        # 1) Set defaults first
        defaults = [110000, 105000, 100000]
        for path, val in zip(TRIP_POINTS_PATHS[::-1], defaults):
            cls._write_values(path, val)

        # 2) Set target values
        for path, val in zip(TRIP_POINTS_PATHS, target_values):
            cls._write_values(path, val)

        return True


if __name__ == "__main__":
    dfs = PciDfsManager()

    logger.debug("\nTesting MAX performance:")
    dfs.set_performance(500.0)
    time.sleep(1)

    logger.debug("\nTesting HIGH performance:")
    dfs.set_performance(250.0)
    time.sleep(1)

    logger.debug("\nTesting MEDIUM performance:")
    dfs.set_performance(125.0)
    time.sleep(1)

    logger.debug("\nTesting LOW performance:")
    dfs.set_performance(62.5)

    dfs.set_performance(500.0)
