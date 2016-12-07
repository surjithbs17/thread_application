import kivy
kivy.require('1.0.6')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


from kivy.uix.screenmanager import ScreenManager, Screen

# Create the manager
sm = ScreenManager()

# Add few screens
for i in range(4):
    screen = Screen(name='Title %d' % i)
    sm.add_widget(screen)



def callback(instance):
    print('The button <%s> is being pressed , ' % instance.text)
    



class LoginScreen(GridLayout):
	def __init__(self,**kwargs):
		super(LoginScreen,self).__init__(**kwargs)
		self.cols = 2
		self.add_widget(Label(text='Enter Label Name'))
		self.device_key = TextInput(multiline=False)
		self.add_widget(self.device_key)

		btn1 = Button(text='Add device')
		btn1.bind(on_press=callback)
		self.add_widget(btn1)
		#self.password = TextInput(password=True, multiline=False)
		#self.add_widget(self.password)
		#self.add_widget(Label(text='Building Brains'))
		#self.userinput = TextInput(multiline = False)
		#self.add_widget(Button(text = 'Enter'))
		#self.add_widget(Button(text = "Hello"))


class MyApp(App):

    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()