from kaki.app import App
from kivy.factory import Factory
from kivy.core.window import Window
import os

Window.size = (360, 640)


class ToDoLive(App):
    CLASSES = {
        "MenuManager": "main",
        "MenuScreen": "main",
        "MultiplayerScreen": "main",
        "T3Main": "main"
    }

    KV_FILES = [os.path.join(os.getcwd(), "tictactoe.kv")]

    AUTORELOADER_PATHS = [
        (os.getcwd(), {"recursive": True})
    ]

    def build_app(self, first=False):
        # self.theme_cls.primary_palette = "Green"
        print("Build App Auto Reload")
        return Factory.MainScreen()


ToDoLive().run()
