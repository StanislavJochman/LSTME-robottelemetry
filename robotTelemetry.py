#!/usr/bin/env python3
import utime
import json

from machine import Pin, PWM
from hcsr04 import HCSR04


class RobotTelemetry:
    def __init__(self, **pins_config):
        '''
        Configure pins.

        All Pins have default preset from robot blueprint.
        Should be used in robot's main program e.g.: 

        from robotTelemetry import RobotTelemetry
        ...
        t = RobotTelemetry(cny_LL=33,...)
        ...

        def main():
            # follow line...
            ...
            t.main()


        Parameters:
            cny_LL (int): Pin number for total left line sensor.
            cny_L (int): Pin number for middle left line sensor.
            cny_M (int): Pin number for total middle line sensor.
            cny_R (int): Pin number for middle right line sensor.
            cny_RR (int): Pin number for total right line sensor.

            ultrasonic_L_trigger (int): Pin number for left ultrasonic sensor trigger.
            ultrasonic_M_trigger (int): Pin number for middle ultrasonic sensor trigger.
            ultrasonic_R_trigger (int): Pin number for right ultrasonic sensor trigger.
            ultrasonic_L_echo (int): Pin number for left ultrasonic sensor echo.
            ultrasonic_M_echo (int): Pin number for middle ultrasonic sensor echo.
            ultrasonic_R_echo (int): Pin number for right ultrasonic sensor echo.

            motor_LF (int): Pin number for left forward motor.
            motor_LB (int): Pin number for left backward motor.
            motor_RF (int): Pin number for right forward motor.
            motor_RB (int): Pin number for right backward motor.
        '''

        self.data = {
            'cny': {},
            'ultrasonic': {},
            'motors': {}
        }

        self.pins_config = pins_config

        self.init_cny()
        self.init_ultrasonic()
        self.init_motors()

    def init_cny(self):
        self.cny = {
            'LL': Pin(self.pins_config.get('cny_LL', 13), Pin.IN),
            'L': Pin(self.pins_config.get('cny_L', 12), Pin.IN),
            'M': Pin(self.pins_config.get('cny_M', 11), Pin.IN),
            'R': Pin(self.pins_config.get('cny_R', 10), Pin.IN),
            'RR': Pin(self.pins_config.get('cny_RR', 9), Pin.IN),
        }

    def read_cny(self):
        for s in self.cny:
            self.data['cny'][s] = self.cny[s].value()

    def init_ultrasonic(self):
        self.ultrasonic = {
            'L': HCSR04(
                trigger_pin=self.pins_config.get('ultrasonic_L_trigger', 14),
                echo_pin=self.pins_config.get('ultrasonic_L_echo', 15)
            ),
            'M': HCSR04(
                trigger_pin=self.pins_config.get('ultrasonic_M_trigger', 4),
                echo_pin=self.pins_config.get('ultrasonic_M_echo', 5)
            ),
            'R': HCSR04(
                trigger_pin=self.pins_config.get('ultrasonic_R_trigger', 2),
                echo_pin=self.pins_config.get('ultrasonic_R_echo', 3)
            ),
        }

    def read_ultrasonic(self):
        for s in self.ultrasonic:
            self.data['ultrasonic'][s] = self.ultrasonic[s].distance_cm()

    def init_motors(self):
        self.motors = {}
        self.motors['LF'] = PWM(Pin(self.pins_config.get('motor_LF', 18)))
        self.motors['LB'] = PWM(Pin(self.pins_config.get('motor_LB', 19)))
        self.motors['RF'] = PWM(Pin(self.pins_config.get('motor_RF', 21)))
        self.motors['RB'] = PWM(Pin(self.pins_config.get('motor_RB', 20)))

    def read_motors(self):
        for m in self.motors:
            self.data['motors'][m] = self.motors[m].duty_u16()

    def json_encode(self):
        return json.dumps(self.data)

    def main(self):
        self.read_cny()
        self.read_ultrasonic()
        self.read_motors()

        print('@start')
        print(self.json_encode())

        utime.sleep(0.01)
