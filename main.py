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


def drawInfo(dist1, dist2, dist3, angle, acc, sensors):
    global c
    #c.create_image((windowsize[0]/2, windowsize[1]/2), image=robotBody)
    #c.create_image((windowsize[0]/2, windowsize[1]-120), image=gyroSensor)
    c.create_text(windowsize[0]/2, windowsize[1]-50, text=angle)
    c.create_text(windowsize[0]/2, windowsize[1]-30, text=acc)
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
    print('WTF', read_telemetry, read_telemetry.data)
    exit(0)


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

    while (end):
        c.delete("all")

        if read_telemetry:
            read_telemetry.consume()

            if read_telemetry.data:
                data = read_telemetry.get_telemetry()

                drawInfo(
                    data['ultrasonic']['L'],
                    data['ultrasonic']['M'],
                    data['ultrasonic']['R'],
                    random.randint(0, 100),
                    random.randint(0, 100),
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
