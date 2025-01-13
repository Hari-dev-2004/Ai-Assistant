from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from android.permissions import request_permissions, Permission

class TicTacToeApp(App):
    def build(self):
        self.title = "Tic Tac Toe"
        layout = BoxLayout(orientation="vertical")
        self.label = Label(text="Tic Tac Toe Game", font_size=30)
        layout.add_widget(self.label)

        # Game Grid
        self.grid = GridLayout(cols=3)
        self.buttons = []
        for i in range(9):
            btn = Button(text="", font_size=40, on_press=self.make_move)
            self.grid.add_widget(btn)
            self.buttons.append(btn)
        layout.add_widget(self.grid)

        # Check permissions on startup
        if platform == "android":
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA])

        return layout

    def make_move(self, instance):
        if instance.text == "":
            instance.text = "X"
            self.label.text = "Your Turn"

        # Add game logic here for Tic-Tac-Toe.

if __name__ == "__main__":
    TicTacToeApp().run()
