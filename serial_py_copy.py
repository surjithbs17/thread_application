import serial 
import time 
port = serial.Serial("/dev/ttyACM0",baudrate=115200, timeout=100.0)

def readlineCR(port):
	rv = port.readline()
	return rv

def get_input():
	input_data = raw_input('Enter the Command:')
	print input_data
	return input_data

while True:
    data = get_input()
    serial_data = "\r\n"+ str(data) + "\r\n"
    #time.sleep(0.0001)
    port.write(serial_data)
    break_flag = True
    while True:
	print "inside while"
	check = get_input()
	rcv = readlineCR(port)
    	print rcv 
	if (check != "\n"):
		break
    #port.write("\r\nYou sent:" + repr(rcv))
