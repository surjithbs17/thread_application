from twisted.internet import protocol, reactor
from parse import *


import serial 
import time 
port = serial.Serial("/dev/ttyAMA0",baudrate=115200, timeout=100.0)

'''
while True:
    port.write("\n")
    #time.sleep(0.0001)
    port.write("info\n")

    rcv = port.read(100)
    print rcv 
    #port.write("\r\nYou sent:" + repr(rcv))
'''





class Echo(protocol.Protocol):
	def dataReceived(self, data):
 		#self.transport.write(data)
 		print data
 		
 		if "ADD" in data:
 			parsed_data = parse("ADD {join_key} {device_name}",data)
 			self.transport.write("ACK")
			#port.write("\n")
			time.sleep(0.1)
			expect_string = "expect "+ parsed_data['join_key']+'\n\n'
			print expect_string

			port.write(expect_string)
			
			port.write("rpi"+ ' " hello"')
			#time.sleep(10)
			#port.write("info")
			while(1):
				rcv = port.read(50)
				print rcv
 		elif "NULL" in data:
 			self.transport.write("ACK")



 		'''
 		if data.startswith("{"):y
 			parsed_json = json.loads(data)
 			print ("\033[1;32;40m Sensor Type ",parsed_json['sensor_name'])
 			print ("\033[1;33;40m Value",parsed_json['Value'])
 			print ("\033[1;34;40m Units",parsed_json['units'])	
		'''

class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
 		return Echo()

reactor.listenTCP(8000, EchoFactory())
reactor.run()
