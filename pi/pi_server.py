from twisted.internet import protocol, reactor
from parse import *


class Echo(protocol.Protocol):
	def dataReceived(self, data):
 		#self.transport.write(data)
 		print data
 		
 		if "ADD" in data:
 			parsed_data = parse("ADD {join_key} {device_name}",data)
 			self.transport.write("ACK")
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
