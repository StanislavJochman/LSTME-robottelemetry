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
        self.cny = {
            'LL': Pin(13, Pin.IN),
            'L': Pin(12, Pin.IN),
            'M': Pin(11, Pin.IN),
            'R': Pin(10, Pin.IN),
            'RR': Pin(9, Pin.IN),
        }

    def read_cny(self):
        for s in self.cny:
            self.data['cny'][s] = self.cny[s].value()

    def init_ultrasonic(self):
        self.ultrasonic = {
            'L': HCSR04(trigger_pin=14, echo_pin=15),
            'M': HCSR04(trigger_pin=4, echo_pin=5),
            'R': HCSR04(trigger_pin=2, echo_pin=3),
        }

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
