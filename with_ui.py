#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


#A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol

connection =None



class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)
        global connection 
        connection = self.transport

        print connection


    def dataReceived(self, data):
        #self.factory.app.print_message(data)
        print data

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        #self.app.print_message("connection lost")
        pass
    def clientConnectionFailed(self, conn, reason):
        #self.app.print_message("connection failed")
        pass


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.listview import ListItemButton
from twisted.internet import reactor, protocol
import pandas as pd
from parse import *

'''


class EchoClient(protocol.Protocol):
    def __init__(self, input):
        self.input = input

    def connectionMade(self):
        self.transport.write(self.input.input)

    def dataReceived(self, data):
        print "Server said:", data
        #reactor.stop()
        #Should I waait?
        #self.transport.loseConnection()
        #reactor.stop()

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

'''

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    GridLayout:
        rows:4        
        Button:
            text: 'Add Device'
            on_press: root.manager.current = 'add_device'
        Button:
            text: 'List Devices'
            on_press: root.manager.current = 'list_device'
        Button:
            text: 'Use Device'
            on_press: root.manager.current = 'use_device'
        
        Button:
            text: 'Quit'
<AddDeviceScreen>:
    GridLayout:
        rows:2
        join_key: join_key
        device_name: device_name
        Button:
            text: 'Add Device'
            on_press: root.add_device_to_list(join_key,device_name)
        TextInput:
            id: device_name
            text: 'device name'
        TextInput:
            id: join_key
            text: 'Join key'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
<ListDeviceScreen>:
    GridLayout:
        rows:2
        Button:
            text: 'In List device'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
<UseDeviceScreen>:
    GridLayout:
        rows:2
        Button:
            text: 'In Use Device'

        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")

application = None
# Declare both screens
class MenuScreen(Screen):
    pass

class UseDeviceScreen(Screen):
    pass

class AddDeviceScreen(Screen):

    def add_device_to_list(self,join_key,device_name):
        add_command_string = "ADD "+ join_key.text + " " + device_name.text
        print add_command_string 
        print connection
        connection.write(add_command_string)



    def text(self, val):
        print('text input text is: {txt}'.format(txt=val))

    pass

class ListDeviceScreen(Screen):
    pass



# Create the screen manager

class TestApp(App):
    
    


    def build(self):
        #root = self.setup_gui()
        self.connect_to_server()
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(UseDeviceScreen(name='use_device'))
        sm.add_widget(AddDeviceScreen(name='add_device'))
        sm.add_widget(ListDeviceScreen(name='list_device'))
        return sm

    
    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, EchoFactory(self))

    def on_connection(self, connection):
        #self.print_message("connected successfully!")
        self.connection = connection

    def send_message(self, *args):
        #msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""

    


    
if __name__ == '__main__':
    
    application = TestApp()
    application.run()