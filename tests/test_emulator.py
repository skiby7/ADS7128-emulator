import os
from time import sleep
import pytest
from smbus2 import SMBus
import subprocess
from ads7128_emulator import ADS7128Emulator

@pytest.fixture(scope="module")
def emulator():
    with ADS7128Emulator() as emu:
        yield emu


def test_initial_values(emulator):
    for channel in range(8):
        assert emulator.read_channel(channel) == 0x000

def test_channel_setting(emulator):
    test_cases = [
        (0, 0x000),   # Minimum value
        (1, 0xFFF),   # Maximum value
        (2, 0x7FF),   # Mid-scale -1
        (3, 0x800),   # Mid-scale
        (4, 0xABC),   # Arbitrary value
        (7, 0x123)    # Last channel
    ]

    for channel, value in test_cases:
        emulator.set_channel(channel, value)

    for channel, value in test_cases:
        assert emulator.read_channel(channel) == value


def test_invalid_channels(emulator):
    with pytest.raises(ValueError):
        emulator.set_channel(-1, 0x800)

    with pytest.raises(ValueError):
        emulator.set_channel(8, 0x800)

def test_invalid_values(emulator):
    with pytest.raises(ValueError):
        emulator.set_channel(0, -1)

    with pytest.raises(ValueError):
        emulator.set_channel(0, 0x1000)

def test_module_cleanup():
    with ADS7128Emulator() as emu:
        assert "smbus stub driver" in subprocess.check_output(["sudo", "i2cdetect", "-l"], text=True).lower()

    assert "smbus stub driver" in subprocess.check_output(["sudo", "i2cdetect", "-l"], text=True).lower()
