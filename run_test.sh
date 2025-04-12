#!/bin/bash

sudo pip install smbus2 &> /dev/null
sudo PYTHONPATH=src/ads7128_emulator:src:$PYTHONPATH -E pytest tests/test_emulator.py -v
