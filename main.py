import kivy
from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(selfself):
        return Label(text="Tech With Tim")


if __name__ == "__main__":
    MyApp().run()

