import subprocess
import time
from smbus2 import SMBus, i2c_msg

class ADS7128Emulator:
    def __init__(self, i2c_address=0x16):
        self.i2c_address = i2c_address
        self.bus_number = None
        self.smbus = None
        self._unload_stub()
        self._load_stub()
        self._find_stub_bus()
        self._initialize_bus()

    def _unload_stub(self):
        subprocess.run(['sudo', 'modprobe', '-r', 'i2c-stub'],
                      stderr=subprocess.DEVNULL)

    def _load_stub(self):
        result = subprocess.run(
            [
                'sudo',
                'modprobe',
                'i2c-stub',
                f'chip_addr={self.i2c_address}',
                'reg_bytes=1',
                'data_bytes=1',
                'reg_max=15',
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

    def _find_stub_bus(self):
        result = subprocess.run(['i2cdetect', '-l'],
                               capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'smbus stub driver' in line.lower():
                self.bus_number = int(line.split()[0].split('-')[1])
                return
        raise RuntimeError("Failed to find i2c-stub bus")

    def _initialize_bus(self):
        self.smbus = SMBus(self.bus_number)
        for ch in range(8):
            self.set_channel(ch, 0x000)

    def set_channel(self, channel: int, value: int):
        if not 0 <= channel <= 7:
            raise ValueError("Channel must be 0-7")
        if not 0 <= value <= 0xFFF:
            raise ValueError("Value must be 0-4095")
        if self.smbus is None:
            raise Exception("smbus driver not initialized correctly")

        msb_reg = channel * 2
        lsb_reg = channel * 2 + 1

        msb = (value >> 4) & 0xFF
        lsb = (value & 0x0F) << 4

        self.smbus.write_byte_data(self.i2c_address, msb_reg, msb)
        self.smbus.write_byte_data(self.i2c_address, lsb_reg, lsb)

    def read_channel(self, channel: int):
        if self.smbus is None:
            raise Exception("smbus driver not initialized correctly")

        msb_reg = channel * 2
        lsb_reg = channel * 2 + 1

        msb = self.smbus.read_byte_data(self.i2c_address, msb_reg)
        lsb = self.smbus.read_byte_data(self.i2c_address, lsb_reg)

        return (msb << 4) | (lsb >> 4)

    def close(self):
        if self.smbus:
            self.smbus.close()
        self._unload_stub()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
