from twisted.internet import protocol, reactor
from parse import *

import serial 
import time 
port = serial.Serial("/dev/ttyUSB0",baudrate=115200, timeout=100.0)


 

def readlineCR(port):
	rv = port.readline()
	return rv

class Echo(protocol.Protocol):
	def dataReceived(self, data):
 		#self.transport.write(data)
 		print data
 		
 		if "ADD" in data:
			#ADD "DFGRU" "LAMP"
 			parsed_data = parse("ADD {join_key} {device_name}",data)
 			self.transport.write("ACK")
			#port.write("\n")
			time.sleep(0.1)
			expect_string = "expect "+ parsed_data['join_key']+'\n\n'
			print expect_string
			
			port.write("\r\n")
			#port.write(LF)
			time.sleep(1)
			new_str = "info\r\n"
			time.sleep(1)
			print "after crlf"
			port.write(new_str)
			#port.write("\r\n")
			print "info printed"
			while True:
				for i in range(0,14):
					rcv = readlineCR(port)
					print rcv
				port.write(new_str)
				time.sleep(1)
				#port.write("\r\nYou sent:" + repr(rcv))
		# rpi "0 0 0 0 0 0 0 " - read temp from device 0
		# MFPI:"2 0 0 0 30 0 " 
		# rpi "0 0 2 0 0 0 0 " - read IP from all clients
		# rpi "0 3 1 2 0 0 0 " - ON actuator
		# rpi "0 3 1 2 0 1 0 " - OFF actuator
		# rpi "0 3 1 3 0 0 0 " - ON LED
		# rpi "0 3 1 3 0 0 0 " - OFF LED

	 
	
 		elif "ACTUATE" in data:
			# ACTUATE <DEVICE_ID> <SENSORID> <ON/OFF> 
			parsed_data = parse{"ACTUATE {DEVICE_ID} {ON_OFF}",data}
			if parsed_data['DEVICE_ID'] is ('0' or '1') :
				#Add device ip or id to send your
				if parsed_data['ON_OFF'] is 'ON':
					send_string = "\r\n"+'rpi "0 3 1 2 0 0'+ parsed_data['DEVICE_ID']+'"' + "\r\n"
					print send_string
					port.write(send_string)		
					#send ON command deviceid
				elif parsed_data['ON_OFF'] is 'OFF':
					send_string = "\r\n"+'rpi "0 3 1 2 0 1'+ parsed_data['DEVICE_ID']+'"' + "\r\n"
					print send_string
					port.write(send_string)
				#send off command to device id 
		elif "LED" in data:
             # ACTUATE <DEVICE_ID> <SENSORID> <ON/OFF>
            parsed_data = parse{"LED {DEVICE_ID} {ON_OFF}",data}
            if parsed_data['DEVICE_ID'] is ('0' or '1') :
                    #Add device ip or id to send your
                    if parsed_data['ON_OFF'] is 'ON':
                    	send_string = "\r\n"+'rpi "0 3 1 3 0 0'+ parsed_data['DEVICE_ID']+'"' + "\r\n"
						print send_string
						port.write(send_string)
                            #send ON command deviceid
                    elif parsed_data['ON_OFF'] is 'OFF':
                        send_string = "\r\n"+'rpi "0 3 1 3 0 1'+ parsed_data['DEVICE_ID']+'"' + "\r\n"
						print send_string
						port.write(send_string)
                        
                        #send off command to device id
		 elif "READ" in data:
            # ACTUATE <Device if
            parsed_data = parse{"READ {DEVICE_ID}",data}
            if parsed_data['DEVICE_ID'] is ('0' or '1') :
                    send_string = "\r\n"+'rpi "0 0 0 0 0 0'+ parsed_data['DEVICE_ID']+'"' + "\r\n"
					print send_string
					port.write(send_string)
'''
 *Start Byte|Main Source    |Command      |interface    |sub interface     |interface Id        |IP         |data                |STOP
	$        0 - Ras Pi	      Read - 0     Sensor -0	 Sensor_temp -0     Sensor#0	        <Optional>   <Sensor Read Data>   '#'
             1 - Client       Reply -1	   Act -1		 Sensor_hum  -1
             2 - Server       Write -2	   Acquire IP -2 Act         -2
            /Bouder Router   Execute -3
'''
			 
		
			 
 			self.transport.write("ACK")
		elif "READ_SENSOR" in data:


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
