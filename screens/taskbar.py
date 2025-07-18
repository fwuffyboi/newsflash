import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
import time


def get_time():
    return time.strftime("%H:%M:%S")


class Taskbar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.time_label = Label(text=get_time())
        self.add_widget(self.time_label)
        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, dt):
        self.time_label.text = get_time()