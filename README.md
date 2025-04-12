# Introduction

A small library to emulate the ADS7128 i2c device using i2c-stub

# Examples

```python
with ADS7128Emulator() as emulator:
    # Set channel 0 to 1V (assuming 3.3V range)
    emulator.set_channel(0, int(1/3.3 * 4095))

    # Read channel 0 value
    value = emulator.read_value(0)
    print(value)

    # Set channel 1 to max value
    emulator.set_channel(1, 0xFFF)

    # Read channel 1 value
    value = emulator.read_value(1)
    print(value)

    print("Emulator ready on bus", emulator.bus_number)
    input("Press Enter to exit...")
```
