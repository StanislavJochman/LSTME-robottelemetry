#!/usr/bin/env python3
import serial
import json


class ReadTelemetry:
    def __init__(self, bluetooth_com_port):
        self.ser = serial.Serial(bluetooth_com_port, 9600, timeout=0,
                                 parity=serial.PARITY_EVEN, rtscts=1)
        self.data = None

        self.buffer = b''
        self.i = 1
        self.initialized = False

    def consume(self):
        '''
        Reads telemtry data from serial port.

        Updates last robot telemetry values.
        Should be used in robot's GUI telemetry main program e.g.:

        import ReadTelemetry
        ...
        t = ReadTelemetry('/dev/tty.usbmodem0000000000001')
        ...

        def draw():
            ...
            t.consume()
            ...
            # draw componets...
            display_values(t.get_telemetry())
        '''

        self.buffer += self.ser.read(100)
        ix = self.buffer.find(b'\r\n')

        if ix > -1:
            row_data = self.buffer[:ix]
            self.buffer = self.buffer[ix+2:]

            row_str = row_data.decode()

            if row_str == '@start':
                if not self.initialized:
                    print('==INITIALIZED==')
                self.initialized = True
                return

            if not self.initialized:
                return

            print('{}. {}'.format(self.i, row_str))
            self.data = json.loads(row_str)
            self.i += 1

    def get_telemetry(self):
        return self.data
