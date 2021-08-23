#!/usr/bin/env python3
import serial
import json


class ReadTelemetry:
    def __init__(self, bluetooth_com_port):
        self.ser = serial.Serial(bluetooth_com_port, 9600, timeout=0,
                                 parity=serial.PARITY_EVEN, rtscts=1)
        self.data = None

    def start_telemetry(self):
        buffer = b''
        i = 1
        initialized = False

        while True:
            buffer += self.ser.read(100)
            ix = buffer.find(b'\r\n')

            if ix > -1:
                row_data = buffer[:ix]
                buffer = buffer[ix+2:]

                row_str = row_data.decode()

                if row_str == '@start':
                    if not initialized:
                        print('==INITIALIZED==')
                    initialized = True
                    continue

                if not initialized:
                    continue

                print('{}. {}'.format(i, row_str))
                self.data = json.loads(row_str)
                i += 1

    def get_telemetry(self):
        return self.data
