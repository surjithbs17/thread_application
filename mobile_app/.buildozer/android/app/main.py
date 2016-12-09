#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
#from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.listview import ListItemButton
from twisted.internet import reactor, protocol
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.properties import (StringProperty, ObjectProperty, OptionProperty,
                             NumericProperty, ListProperty)

from parse import *



#A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol

connection =None



def data_processor(data):
    # create content and add to the popup
    content = Button(text=data)
    popup = Popup(content=content, auto_dismiss=False)

# bind the on_press event of the button to the dismiss function
    content.bind(on_press=popup.dismiss)

# open the popup
    popup.open()


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        #self.factory.app.on_connection(self.transport)
        global connection 
        connection = self.transport
        print connection


    def dataReceived(self, data):
        #self.factory.app.print_message(data)
        data_processor(data)



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
            text: 'Use Device'
            on_press: root.manager.current = 'use_device'
        Button:
            text: 'Configure Pi'
            on_press: root.manager.current = 'config_device'
        
        Button:
            text: 'Quit'

<ConfigureDeviceScreen>:
    GridLayout:
        rows:2
        address: address
        port: port
        Button:
            text: 'Configure'
            on_press: root.config_device(address,port)
        TextInput:
            id: address
            text: 'Address'
        TextInput:
            id: port
            text: 'Port Number'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'





<AddDeviceScreen>:
    GridLayout:
        rows:2
        
        Button:
            text: 'Add Device'
            on_press: root.add_device_to_list()
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'

<UseDeviceScreen>:
    GridLayout:
        rows:3
        Button:
            text: 'Device 1'
            on_press: root.manager.current = 'device_1'
        Button:
            text: 'Device 2'
            on_press: root.manager.current = 'device_2'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
<UseDevice_1>:
    GridLayout:
        rows:5
        Button:
            text: 'Relay ON'
            on_press: root.relay_on()
        Button:
            text: 'Relay OFF'
            on_press: root.relay_off()
        Button:
            text: 'Read Temparature'
            on_press: root.read_temp()
        Button:
            text: 'Read Humidity'
            on_press: root.read_humi()        
        Button:
            text: 'Back to Device'
            on_press: root.manager.current = 'use_device'
<UseDevice_2>:
    GridLayout:
        rows:5
        Button:
            text: 'Relay ON'
            on_press: root.relay_on()
        Button:
            text: 'Relay OFF'
            on_press: root.relay_off()
        Button:
            text: 'Read Temparature'
            on_press: root.read_temp()
        Button:
            text: 'Read Humidity'
            on_press: root.read_humi()
        Button:
            text: 'Back to Device'
            on_press: root.manager.current = 'use_device'
""")

class MenuScreen(Screen):
    pass

class ConfigureDeviceScreen(Screen):
    def config_device(self,address,port):
        #add_command_string = "ADD "+ join_key.text + " " + device_name.text
        reactor.connectTCP(address.text, int(port.text), EchoFactory(self))
    pass

class UseDeviceScreen(Screen):
    pass


class UseDevice_1(Screen):
    def relay_on(self):
        message = "ACTUATE 0 ON"
        print connection
        connection.write(message)

    def relay_off(self):
        message = "ACTUATE 0 OFF"
        print connection
        connection.write(message)

    def read_temp(self):
        message = "READ 0 TEMP"
        print connection
        connection.write(message)

    def read_humi(self):
        message = "READ 0 HUMI"
        print connection
        connection.write(message)

class UseDevice_2(Screen):
    def relay_on(self):
        message = "ACTUATE 1 ON"
        print connection
        connection.write(message)
        #temp_popup("Relay Actuated").popup.open()


    def relay_off(self):
        message = "ACTUATE 1 OFF"
        print connection
        connection.write(message)

    def read_temp(self):
        message = "READ 1 TEMP"
        print connection
        connection.write(message)

    def read_humi(self):
        message = "READ 1 HUMI"
        print connection
        connection.write(message)



class AddDeviceScreen(Screen):

    def add_device_to_list(self):
        add_command_string = "ADD"
        print add_command_string 
        print connection
        connection.write(add_command_string)






# Create the screen manager

class TestApp(App):

    def build(self):
        #root = self.setup_gui()
        #self.connect_to_server()
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(UseDeviceScreen(name='use_device'))
        sm.add_widget(UseDevice_1(name='device_1'))
        sm.add_widget(UseDevice_2(name='device_2'))
        sm.add_widget(AddDeviceScreen(name='add_device'))
        sm.add_widget(ConfigureDeviceScreen(name='config_device'))

        return sm
    
    def connect_to_server(self):
        reactor.connectTCP('127.0.0.1', 8000, EchoFactory(self))

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