#!/usr/bin/env python3
import json
import sys


def telemetry(**values):
    '''
    The function for sending telemetry data.

    Prints data on standard output.
    Should be used in robot's main program loop e.g.:
        def main():
            # follow line...
            ...
            telemetry(cny_LL=r.cny['LL'], ...)

    Parameters:
        cny_LL (int): Value for total left line sensor. 0 when reads black, 1 when reads white.
        cny_L (int): Value for middle left line sensor. 0 when reads black, 1 when reads white.
        cny_M (int): Value for total middle line sensor. 0 when reads black, 1 when reads white.
        cny_R (int): Value for middle right line sensor. 0 when reads black, 1 when reads white.
        cny_RR (int): Value for total right line sensor. 0 when reads black, 1 when reads white.

        ultrasonic_L (float): Value for left ultrasonic sensor. Distance in centimeters.
        ultrasonic_M (float): Value for middle ultrasonic sensor. Distance in centimeters.
        ultrasonic_R (float): Value for right ultrasonic sensor. Distance in centimeters.

        motor_LF_freq (int): Left forward motor's PWM frequency.
        motor_LF_duty (int): Left forward motor's PWM duty cycle (uint16).
        motor_LB_freq (int): Left backward motor's PWM frequency.
        motor_LB_duty (int): Left backward motor's PWM duty cycle (uint16).
        motor_RF_freq (int): Right forward motor's PWM frequency.
        motor_RF_duty (int): Right forward motor's PWM duty cycle (uint16).
        motor_RB_freq (int): Right backward motor's PWM frequency.
        motor_RB_duty (int): Right backward motor's PWM duty cycle (uint16).
    '''

    data = {
        'cny': {
            'LL': values['cny_LL'],
            'L': values['cny_L'],
            'M': values['cny_M'],
            'R': values['cny_R'],
            'RR': values['cny_RR'],
        },
        'ultrasonic': {
            'L': values['ultrasonic_L'],
            'M': values['ultrasonic_M'],
            'R': values['ultrasonic_R'],
        },
        'motors':   {
            'LF': {
                'freq': values['motor_LF_freq'],
                'duty': values['motor_LF_duty']
            },
            'LB': {
                'freq': values['motor_LB_freq'],
                'duty': values['motor_LB_duty']
            },
            'RF': {
                'freq': values['motor_RF_freq'],
                'duty': values['motor_RF_duty']
            },
            'RB': {
                'freq': values['motor_RB_freq'],
                'duty': values['motor_RB_duty']
            }
        }
    }

    json_data = json.dumps(data)
    read_bytes = sys.getsizeof(json_data).to_bytes(64, 'little')

    print('@'.encode(), end='')
    # print(read_bytes, end='')
    # print(json_data, end='')
