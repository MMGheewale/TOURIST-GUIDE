from kivy.uix.screenmanager import Screen
import home
from kivy.app import App

class BlankScreen(Screen):
    def gotohome(self):
        print("go to home")
        App().get_running_app().stop()
        home.home()
