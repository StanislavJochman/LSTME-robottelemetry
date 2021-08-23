import serial
import time

data = []
def connect(port):
    serial_port = serial.Serial(port, 9600)
    return serial_port
       
def ReadSerial(ser):
    global data
    datatmp = []
    data_str = str(ser.readline().decode())
    if(data_str[:-2] == "@"):
        datatmp = data
        data = []
        return datatmp
    elif(data_str != ""):
        data.append(data_str[:-2])

if __name__ == "__main__":
    ser = connect("/dev/ttyACM0")
    ser.flushInput()
    while True:
        data_ser = ReadSerial(ser) 
        if(data_ser != None):
            print(data_ser)
        