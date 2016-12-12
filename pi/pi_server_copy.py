from twisted.internet import protocol, reactor
from parse import *

import serial 
import time 
port = serial.Serial("/dev/ttyACM0",baudrate=115200, timeout=100.0)
'''
class check:
	
	def write(self,input):
		print input


def readlineCR():
		return "MFPI:BOUND 0"


port = check()
'''


def readlineCR():
	rv = port.readline()
	return rv

class Echo(protocol.Protocol):
	def dataReceived(self, data):
 		#self.transport.write(data)
 		print data
 		#parsed_data
 		if 'ADD' in data:
			port.write("\n")
			time.sleep(0.1)
			expect_string_1 = 'expect "BLBTUCB0"\r\n'
			expect_string_2 = 'expect "4GBTUCB0"\r\n'
			reply_1 = dict()
			reply_2 = dict()

			print expect_string_1
			print expect_string_2
			port.write(expect_string_1)
			while True:
				msg_from_server = readlineCR()
				print msg_from_server
				if "MFPI:BOUND" in msg_from_server:
					reply_1 = parse("MFPI:BOUND {DEVICE_ID}",msg_from_server)
					print "Inside Bound"
					self.transport.write('Bound Success 1 "BLBTUCB0"')
					break

			port.write(expect_string_2)
			while True:
				msg_from_server = readlineCR()
				print msg_from_server

				if "MFPI:BOUND" in msg_from_server:
					reply_2 = parse("MFPI:BOUND {DEVICE_ID}",msg_from_server)
					print "Inside Second Bound"
					self.transport.write('Bound Success 1 "4GBTUCB0"')
					break

			reply_string = "DEVICE 1 Paired as %s \n DEVICE 2 Paired as %s\n"%(reply_1['DEVICE_ID'],reply_2['DEVICE_ID']) 
			
			print reply_string
			#have to send acquire IP command
			self.transport.write(reply_string)

		if 'LED' in data:
			# ACTUATE <DEVICE_ID> <SENSORID> <ON/OFF> 
			parsed_data = parse("LED {DEVICE_ID} {ON_OFF}",data)
			
			if (parsed_data['DEVICE_ID'] is ('0')) or (parsed_data['DEVICE_ID'] is ('1')) :
				#Add device ip or id to send your
				print "Inside parsed"
				if 'ON' in parsed_data['ON_OFF']:
					print "Inside ON"
					send_string = "\r\n"+'rpi "$ 0 3 1 3 0 0 '+ parsed_data['DEVICE_ID']+' #"' + "\r\n"
					print send_string
					port.write(send_string)		
					#send ON command deviceid
				elif 'OFF' in parsed_data['ON_OFF']:
					print "Inside OFF"
					send_string = "\r\n"+'rpi "$ 0 3 1 3 0 1 '+ parsed_data['DEVICE_ID']+' #"' + "\r\n"
					print send_string
					port.write(send_string)
			while True:
				msg_from_server = readlineCR()
				if "MFPI" in msg_from_server:
					if 'ON' in parsed_data['ON_OFF']:
						self.transport.write('LED Turned ON')
						break
					if 'OFF' in parsed_data['ON_OFF']:
						self.transport.write('LED Turned OFF')
						break

		if 'ACTUATE' in data:
			# ACTUATE <DEVICE_ID> <SENSORID> <ON/OFF> 
			parsed_data = parse("ACTUATE {DEVICE_ID} {ON_OFF}",data)
			
			if (parsed_data['DEVICE_ID'] is ('0')) or (parsed_data['DEVICE_ID'] is ('1')) :
				#Add device ip or id to send your
				print "Inside parsed"
				if 'ON' in parsed_data['ON_OFF']:
					print "Inside ON"
					send_string = "\r\n"+'rpi "$ 0 3 1 2 0 0 '+ parsed_data['DEVICE_ID']+' #"' + "\r\n"
					print send_string
					port.write(send_string)		
					#send ON command deviceid
				elif 'OFF' in parsed_data['ON_OFF']:
					print "Inside OFF"
					send_string = "\r\n"+'rpi "$ 0 3 1 2 0 1 '+ parsed_data['DEVICE_ID']+' #"' + "\r\n"
					print send_string
					port.write(send_string)
			while True:
				msg_from_server = readlineCR()
				if "MFPI" in msg_from_server:
					if 'ON' in parsed_data['ON_OFF']:
						self.transport.write('Relay Turned ON')
						break
					if 'OFF' in parsed_data['ON_OFF']:
						self.transport.write('Relay Turned OFF')
						break
		if "READ" in data:
		 	parsed_data = parse("READ {DEVICE_ID} {TYPE}",data)
		 	print parsed_data['DEVICE_ID']
		 	print parsed_data['TYPE']
		 	if (parsed_data['DEVICE_ID'] is ('0')) or (parsed_data['DEVICE_ID'] is ('1')) :
		 		if 'TEMP' in parsed_data['TYPE']:
		 			send_string = "\r\n"+'rpi "$ 0 0 0 0 0 0 '+ parsed_data['DEVICE_ID']+' #"' + "\r\n"
		 			print send_string
		 			port.write(send_string)
				elif 'HUMI' in parsed_data['TYPE']:
					send_string = "\r\n"+'rpi "$ 0 0 0 1 0 0 '+ parsed_data['DEVICE_ID']+' #"' + "\r\n"
					print send_string
					port.write(send_string)

#MFPI:$ 2 0 0 0 0 21 1 #

			while True:
				msg_from_server = readlineCR()
				#msg_from_server = readlineCR()
				print msg_from_server
				if "MFPI" in msg_from_server:
					try:
						msg_string = parse('MFPI: {DATA} {DEVICE_ID}',msg_from_server)
						print msg_string['DATA']
						to_app_reply = "Sensor Data %s \n%s "%(parsed_data['TYPE'],msg_string['DATA'])
						print to_app_reply
						self.transport.write(to_app_reply)
						break
					except TypeError:
						print "Type Error"
						self.transport.write("ERROR")
						break
				
class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
 		return Echo()

reactor.listenTCP(8000, EchoFactory())
reactor.run()
