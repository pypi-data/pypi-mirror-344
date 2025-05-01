# Copyright 2024
# Licensed under the Apache License, Version 2.0

import time
from dfs_interface import create_dfs_manager


def get_available_device_type():
    """Detect which type of Edge TPU device is available.

    Returns:
        str: 'usb', 'pci', or None if no device is found
    """
    from usb_dfs_manager import UsbDfsManager
    from pci_dfs_manager import PciDfsManager

    if UsbDfsManager.detect_device():
        return "usb"
    elif PciDfsManager.detect_device():
        return "pci"
    return None


def print_frequency_info(device_type=None):
    """Print the current frequency information of the Edge TPU.

    Args:
        device_type: 'usb', 'pci', or None (auto-detect)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        manager = create_dfs_manager(device_type)
        info = manager.get_current_frequency()

        print("Edge TPU Frequency Information:")
        print("-" * 30)

        for key, value in info.items():
            print(f"{key}: {value}")

        return True
    except Exception as e:
        print(f"Error getting frequency information: {e}")
        return False


def set_and_verify_frequency(frequency: float, device_type=None):
    """Set the Edge TPU frequency to the specified level and verify the change.

    Args:
        frequency: The desired frequency
        device_type: 'usb', 'pci', or None (auto-detect)

    Returns:
        bool: True if frequency was successfully set and verified, False otherwise
    """
    manager = create_dfs_manager(device_type)

    # Get initial frequency information
    initial_info = manager.get_current_frequency()
    if initial_info["frequency"] == frequency:
        return True

    # Set the new frequency
    print(f"\nSetting frequency to {frequency}...")
    success = manager.set_frequency(frequency)

    if not success:
        print("Failed to set frequency")
        return False

    return True


def run_inference_benchmark(interpreter, num_iterations=10, frequency=None, device_type=None):
    """Run an inference benchmark with optional frequency adjustment.

    Args:
        interpreter: TFLite interpreter with the model loaded
        num_iterations: Number of inference iterations to run
        frequency: Optional frequency to set before benchmarking
        device_type: 'usb', 'pci', or None (auto-detect)

    Returns:
        dict: Benchmark results with timing information
    """
    # Set frequency if requested
    if frequency is not None:
        set_and_verify_frequency(frequency, device_type)

    # Run the benchmark
    durations = []

    for i in range(num_iterations):
        # Run inference and time it
        start_time = time.perf_counter()
        interpreter.invoke()
        end_time = time.perf_counter()

        # Calculate time in milliseconds
        inference_time_ms = (end_time - start_time) * 1000
        durations.append(inference_time_ms)

        print(f"Iteration {i+1}/{num_iterations}: {inference_time_ms:.2f}ms")

    return durations
