#!/usr/bin/env python3
import serial
import json
import sys
import time


class ReadTelemetry:
    def __init__(self, bluetooth_com_port):
        self.ser = serial.Serial(
            bluetooth_com_port, 9600, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

        self.init_buffer = []
        self.init_buffer_max_length = sys.getsizeof('@')  # 50

    def read_telemetry(self):
        self.init_buffer.append(self.ser.read(1))
        self.init_buffer = self.init_buffer[-self.init_buffer_max_length:]

        start_byte = b''.join(self.init_buffer)
        print(start_byte)
        print(start_byte.decode().strip(), len(self.init_buffer))

        if start_byte.decode().strip() != '@':
            return

        print('init')
        exit('OK')

        bytes = self.ser.read(64)
        print('bytes', bytes)  # debug
        read_bytes = int.from_bytes(bytes, 'little')

        data_json = self.ser.read(read_bytes)
        data = json.loads(data_json)

        print(data)  # debug


# test
t = ReadTelemetry('/dev/tty.LSTME20-SPPDev')


while True:
    t.read_telemetry()
