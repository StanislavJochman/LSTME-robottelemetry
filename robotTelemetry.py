#!/usr/bin/env python3

from machine import Pin
from hcsr04 import HCSR04
import json


class RobotTelemetry:
    def __init__(self):
        self.data = {
            'cny': {},
            'ultrasonic': {},
            'motors':   {}
        }

        self.init_cny()
        self.init_ultrasonic()
        self.init_motors()

    def init_cny(self):
        pins = {
            'LL': 13,
            'L': 12,
            'M': 11,
            'R': 10,
            'RR': 9,
        }

        self.cny = {}
        for s in pins:
            self.cny[s] = Pin(pins[s], Pin.IN)

    def read_cny(self):
        for s in self.cny:
            self.data['cny'][s] = self.cny[s].value()

    def init_ultrasonic(self):
        pins = {
            'L': {'trigger': 14, 'echo': 15},
            'M': {'trigger': 4, 'echo': 5},
            'R': {'trigger': 2, 'echo': 3},
        }

        self.ultrasonic = {}
        for s in pins:
            self.ultrasonic[s] = HCSR04(
                trigger_pin=pins[s]['trigger'],
                echo_pin=pins[s]['echo'],
                echo_timeout_us=1000000
            )

    def read_ultrasonic(self):
        for s in self.ultrasonic:
            self.data['ultrasonic'][s] = self.ultrasonic[s].distance_cm()

    def init_motors(self):
        pass

    def read_motors(self):
        pass

    def json_encode(self):
        return json.dumps(self.data)

    def main(self):
        while True:
            self.read_cny()
            self.read_ultrasonic()
            self.read_motors()
            print(self.json_encode())
