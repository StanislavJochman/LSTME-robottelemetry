#!/usr/bin/env python3 
import tkinter
from tkinter import ttk
import sys,os
import readTelemetry
import serial
import serial.tools.list_ports
import time
import random

windowsize = (1280,720)

def open_exit_popup():
   top = tkinter.Toplevel(win)
   top.geometry("200x85")
   top.title("Exit program")
   tkinter.Label(top, text= "Do you want to quit", font=('Mistral 11')).place(x=30,y=0)
   tkinter.Button(top, text= "Yes", command= exit).place(x=40,y=30)
   tkinter.Button(top, text= "No", command= top.destroy).place(x=100,y=30)

def buttonHanlder(event):
    global finish,start,robot
    if(event.char == "\x1b"):
        open_exit_popup()
    else:
        pass    

def drawInfo(dist1,dist2,dist3,angle,acc,sensors):
    global c
    c.create_image((windowsize[0]/2, windowsize[1]/2), image = robotBody)
    c.create_image((windowsize[0]/2, windowsize[1]-120), image = gyroSensor)
    c.create_text(windowsize[0]/2, windowsize[1]-50,text=angle)    
    c.create_text(windowsize[0]/2, windowsize[1]-30,text=acc)    
    c.create_text(windowsize[0]/2, windowsize[1]/2-190,text=dist2)    
    c.create_text(windowsize[0]/2-120, windowsize[1]/2-150,text=dist1)    
    c.create_text(windowsize[0]/2+120, windowsize[1]/2-150,text=dist3)
    for x in range(5):
        if(sensors[x] == 1):
            c.create_rectangle(windowsize[0]/2-125+x*50, 30, windowsize[0]/2+(x*50)-75, 80,fill='black',outline='black')
        else:
            c.create_rectangle(windowsize[0]/2-125+x*50, 30, windowsize[0]/2+(x*50)-75, 80,fill='white',outline='black')
      

    

if __name__ == "__main__":
    print(os.getcwd())
    win = tkinter.Tk(className='Robot telemetry')
    win.geometry("{}x{}".format(windowsize[0],windowsize[1]))
    c = tkinter.Canvas(win,width=windowsize[0]+20, height=windowsize[1]+20, background= "white")
    lightSensor = tkinter.PhotoImage(file="./img/cny70.png")
    lightSensor = lightSensor.subsample(3, 3)
    gyroSensor = tkinter.PhotoImage(file="./img/gyro.png")
    gyroSensor= gyroSensor.subsample(3, 3)
    motor = tkinter.PhotoImage(file="./img/motor.png")
    motor = motor.subsample(3, 3)
    ultrasonicSensor = tkinter.PhotoImage(file="./img/ultrasonic.png")
    ultrasonicSensor = ultrasonicSensor.subsample(3, 3)
    robotBody = tkinter.PhotoImage(file="./img/robot.png")
    robotBody = robotBody.subsample(1, 1)
    win.bind('<KeyPress>',buttonHanlder)
    win.resizable(width=False, height=False)


def getComPort():
    print(variable.get())

if __name__ == "__main__":


    variable = tkinter.StringVar(win)
    variable.set("Serial port") # default value
    

    portlist = ["Serial port"]
    ports = serial.tools.list_ports.comports()
    for p in ports:
        portlist.append(p.device)
    print(portlist)

    dropdown = tkinter.OptionMenu(win, variable, *portlist).place(x=0,y=0)
    tkinter.Button(win, text= "Connect",pady=5,fg="gray", command=getComPort ).place(x=107,y=0)    
    

    starttime = time.time()
    lightArr = [0,0,0,0,0]
    while True:
        c.delete("all")
        if (time.time()-starttime>0.1):
            lightArr = []
            for x in range(5):
                lightArr.append(random.randint(0,1))
            print(lightArr)
            starttime = time.time()
        
        drawInfo(random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,360),random.randint(0,1),lightArr)
        c.pack()
        c.update()
        time.sleep(0.04)
        