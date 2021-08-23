#!/usr/bin/env python3
import tkinter
from tkinter import ttk
import sys
import os
import serial
import serial.tools.list_ports
import time
import random

from readTelemetry import ReadTelemetry

windowsize = (1280, 720)

end = 1


def buttonHanlder(event):
    global end
    if(event.char == "\x1b"):
        end = 0
        exit()
    else:
        pass

# drawing info on screen


def drawInfo(dist1, dist2, dist3, angle, l_motor, r_motor, sensors):
    global c
    #c.create_image((windowsize[0]/2, windowsize[1]/2), image=robotBody)
    #c.create_image((windowsize[0]/2, windowsize[1]-120), image=gyroSensor)
    c.create_text(windowsize[0]/2, windowsize[1]-50, text=angle)
    c.create_text(windowsize[0]/2-120, windowsize[1]-30, text=l_motor)
    c.create_text(windowsize[0]/2+120, windowsize[1]-30, text=r_motor)
    c.create_text(windowsize[0]/2, windowsize[1]/2-190, text=dist2)
    c.create_text(windowsize[0]/2-120, windowsize[1]/2-150, text=dist1)
    c.create_text(windowsize[0]/2+120, windowsize[1]/2-150, text=dist3)
    for x in range(5):
        if(sensors[x] == 1):
            c.create_rectangle(
                windowsize[0]/2-125+x*50, 30, windowsize[0]/2+(x*50)-75, 80, fill='white', outline='black')
        else:
            c.create_rectangle(
                windowsize[0]/2-125+x*50, 30, windowsize[0]/2+(x*50)-75, 80, fill='black', outline='black')


if __name__ == "__main__":
    win = tkinter.Tk(className='Robot telemetry')
    win.geometry("{}x{}".format(windowsize[0], windowsize[1]))
    c = tkinter.Canvas(
        win, width=windowsize[0]+20, height=windowsize[1]+20, background="white")
    #lightSensor = tkinter.PhotoImage(file="./img/cny70.png")
    #lightSensor = lightSensor.subsample(3, 3)
    # gyroSensor = tkinter.PhotoImage(file="./img/gyro.png")
    # gyroSensor = gyroSensor.subsample(3, 3)
    # motor = tkinter.PhotoImage(file="./img/motor.png")
    # motor = motor.subsample(3, 3)
    # ultrasonicSensor = tkinter.PhotoImage(file="./img/ultrasonic.png")
    # ultrasonicSensor = ultrasonicSensor.subsample(3, 3)
    # robotBody = tkinter.PhotoImage(file="./img/robot.png")
    # robotBody = robotBody.subsample(10, 10)
    win.bind('<KeyPress>', buttonHanlder)
    win.resizable(width=False, height=False)

read_telemetry = None


def getComPort():
    global read_telemetry
    read_telemetry = ReadTelemetry(variable.get())


if __name__ == "__main__":
    variable = tkinter.StringVar(win)
    variable.set("Serial port")
    # list for storing serial ports
    portlist = ["Serial port"]
    ports = serial.tools.list_ports.comports()
    # adding ports to list
    for p in ports:
        portlist.append(p.device)

    # dropdown menu
    tkinter.OptionMenu(win, variable, *portlist).place(x=0, y=0)
    tkinter.Button(win, text="Connect", pady=5, fg="gray",
                   command=getComPort).place(x=107, y=0)

    starttime = time.time()

    motor_start_threshold = 40_000
    motor_max = 2 ** 16 - 1 - motor_start_threshold

    while (end):
        c.delete("all")

        if read_telemetry:
            read_telemetry.consume()

            if read_telemetry.data:
                data = read_telemetry.get_telemetry()

                lm = 'LF' if data['motors']['LF'] > data['motors']['LB'] else 'LB'
                rm = 'RF' if data['motors']['RF'] > data['motors']['RB'] else 'RB'

                if data['motors'][lm] < motor_start_threshold:
                    l_value = motor_start_threshold
                else:
                    l_value = data['motors'][lm]
                if data['motors'][rm] < motor_start_threshold:
                    r_value = motor_start_threshold
                else:
                    r_value = data['motors'][rm]

                l_motor = (l_value - motor_start_threshold) / motor_max * 100
                r_motor = (r_value - motor_start_threshold) / motor_max * 100

                dir_l = -1 if lm == 'LB' else 1
                dir_r = -1 if rm == 'RB' else 1

                l_motor *= dir_l
                r_motor *= dir_r

                print('LF', data['motors']['LF'])
                print('LB', data['motors']['LB'])
                print('RF', data['motors']['RF'])
                print('RB', data['motors']['RB'])

                drawInfo(
                    data['ultrasonic']['L'],
                    data['ultrasonic']['M'],
                    data['ultrasonic']['R'],
                    random.randint(0, 100),
                    '{:3.2f}%'.format(l_motor),
                    '{:3.2f}%'.format(r_motor),
                    [
                        data['cny']['LL'],
                        data['cny']['L'],
                        data['cny']['M'],
                        data['cny']['R'],
                        data['cny']['RR']
                    ]
                )
        c.pack()
        c.update()
        time.sleep(0.04)
