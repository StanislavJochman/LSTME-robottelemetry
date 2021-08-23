#!/usr/bin/python
from ui import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut, QLabel, QHBoxLayout
import sys
import serial.tools.list_ports
import robotdata
import time

ComPort = ""
data_ser = []
connected = 0
ser = None
def setupButtons(objName, WindowName):
	ui = objName
	ui.ConnectButton.clicked.connect(lambda: Connect(ui))
	objName.KeyF = QShortcut(QKeySequence('w'), WindowName)
	objName.KeyF.activated.connect(lambda: sendDir("w"))
	objName.KeyB = QShortcut(QKeySequence('s'), WindowName)
	objName.KeyB.activated.connect(lambda: sendDir("s"))
	objName.KeyL = QShortcut(QKeySequence('a'), WindowName)
	objName.KeyL.activated.connect(lambda: sendDir("a"))
	objName.KeyR = QShortcut(QKeySequence('d'), WindowName)
	objName.KeyR.activated.connect(lambda: sendDir("d"))
	 
def Connect(ui):
	global ComPort
	ComPort = ui.COM_Port.currentText()
	
def sendDir(dir):
	if(dir == "w"):
		print("w")
	elif(dir == "s"):
		print("s")
	elif(dir == "a"):
		print("a")
	elif(dir == "d"):
		print("d")

def updateData():
	global data_ser,ser,connected
	
	if(ComPort != ""):
		if(connected == 0):
			ser = robotdata.connect(ComPort)
			connected = 1
		else:
			data_ser = robotdata.ReadSerial(ser)
			if(data_ser != None and len(data_ser) != 0 and len(data_ser) == 16):
				ui.LightSensor1.setValue(int(data_ser[0]))
				ui.LightSensor2.setValue(int(data_ser[1]))
				ui.LightSensor3.setValue(int(data_ser[2]))
				ui.LightSensor4.setValue(int(data_ser[3]))
				ui.LightSensor5.setValue(int(data_ser[4]))
				ui.Ultrasonic1.display(int(data_ser[5]))
				ui.Ultrasonic2.display(int(data_ser[6]))
				ui.Ultrasonic3.display(int(data_ser[7]))
				ui.MotorR.display(int(data_ser[8]))
				ui.MotorL.display(int(data_ser[9]))
				ui.GyroX.display(int(data_ser[10]))
				ui.GyroY.display(int(data_ser[11]))
				ui.GyroZ.display(int(data_ser[12]))
				ui.AccelerometerX.display(float(data_ser[13]))
				ui.AccelerometerY.display(float(data_ser[14]))
				ui.AccelerometerZ.display(float(data_ser[15]))



	QtCore.QTimer.singleShot(5, updateData)

if __name__ == "__main__":
	ports = serial.tools.list_ports.comports()
	app = QtWidgets.QApplication(sys.argv)
	TelemetryWindow = QtWidgets.QMainWindow()
	ui = Ui_Dialog()
	ui.setupUi(TelemetryWindow)
	portlist = ["Serial port"]
	ports = serial.tools.list_ports.comports()
	for p in ports:
		portlist.append(p.device)
		ui.COM_Port.addItem(p.device)
	setupButtons(ui,TelemetryWindow)
	TelemetryWindow.show()
	
	QtCore.QTimer.singleShot(5, updateData)
	sys.exit(app.exec_())