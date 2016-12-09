from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
	def __init__(self, input):
 		self.input = input

 	def connectionMade(self):
 		self.transport.write(self.input.input)

	def dataReceived(self, data):
 		print "Server said:", data
 		self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory):
 	def __init__(self, input):
 		self.input = input

 	def buildProtocol(self, addr):
 		return EchoClient(self)
 
 	def clientConnectionFailed(self, connector, reason):
 		print "Connection failed."
 		reactor.stop()
 
 	def clientConnectionLost(self, connector, reason):
 		print "Connection lost."
 		reactor.stop()


reactor.connectTCP("localhost", 8000, EchoFactory("Hello Asshole"))
reactor.run()