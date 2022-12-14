# TIC TAC TOE
import socket
import threading
# import pickle
# from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen


class MenuManager(ScreenManager):
    pass


class MenuScreen(Screen):
    pass


class MultiplayerScreen(Screen):
    host = socket.gethostname()
    port = 55783

    def __init__(self, **kwargs):
        super(MultiplayerScreen, self).__init__(**kwargs)
        self.player2 = None
        self.addr = None

    def host_game(self):
        # self.ids.connectivity.text = f"Connected to address: "
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((self.host, self.port))
            self.ids.host.disabled = True
            self.ids.join.disabled = True
            print("Server started")
            server.listen(1)
            self.ids.conn.text = "Server Started, waiting for connection..."
        except Exception as e:
            self.ids.conn.text = str(e)
            print(e)

        # server.listen(1)
        # self.ids.conn.text = "Server Started, waiting for connection..."
        # print("Server Listening")

        #self.player2, self.addr = server.accept()
        # print("Server Connected to by Opponent)
        # print(self.ids.conn.text)
        # while True:
        #     threading.Thread(target=self.connection_handler, args=(player2,)).start()

    def join(self):
        player2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            player2.connect((self.host, self.port))
            self.ids.status.text = f"Successfully connected to server, the host is assigned X"
            # print("Successfully connected to server\n"
            #       "The host is auto assigned X")
            threading.Thread(target=self.connection_handler, args=(player2,)).start()
        except Exception as e:
            print(e)
            self.ids.status.text = str(e)

    def connection_handler(self, player2):
        self.move = "X"
        while True:
            if self.move == "X":
                move1 = input("Enter your move: ")
                self.move = "O"
                player2.send(move1.encode("utf-8"))
                print("Sent " + move1)
            else:
                data = player2.recv(1024)
                if not data:
                    print("disconnected")
                    break
                else:
                    move2 = data.decode("utf-8")
                    print("Received: " + move2)
                    self.move = "X"
        print("Lost connection")
        player2.close()


class T3Main(MultiplayerScreen):
    def __init__(self, **kwargs):
        super(T3Main, self).__init__(**kwargs)
        self.turn = "X"
        self.count = 1
        self.button = ObjectProperty()
        self.move = ""

    # Game Logic
    def game_rules(self):
        # Across
        for i in range(1, 8, 3):
            if self.ids['b'+str(i)].text != "" and self.ids['b'+str(i)].text == self.ids['b'+str(i+1)].text \
                    and self.ids['b'+str(i+1)].text == self.ids['b'+str(i+2)].text:
                self.ids['b'+str(i)].color = "green"
                self.ids['b'+str(i+1)].color = "green"
                self.ids['b'+str(i+2)].color = "green"
                self.end_game()
        # Down
        for i in range(1, 4):
            if self.ids['b'+str(i)].text != "" and self.ids['b'+str(i)].text == self.ids['b'+str(i+3)].text \
                    and self.ids['b'+str(i+3)].text == self.ids['b'+str(i+6)].text:
                self.ids['b'+str(i)].color = "green"
                self.ids['b'+str(i+3)].color = "green"
                self.ids['b'+str(i+6)].color = "green"
                self.end_game()
        # Diagonal
        for i in range(1, 4, 2):
            if i == 1:
                if self.ids['b'+str(i)].text != "" and self.ids['b'+str(i)].text == self.ids['b'+str(i+4)].text \
                        and self.ids['b'+str(i+4)].text == self.ids['b'+str(i+8)].text:
                    self.ids['b'+str(i)].color = "green"
                    self.ids['b'+str(i+4)].color = "green"
                    self.ids['b'+str(i+8)].color = "green"
                    self.end_game()
            elif i == 3:
                if self.ids['b'+str(i)].text != "" and self.ids['b'+str(i)].text == self.ids['b'+str(i+2)].text \
                        and self.ids['b'+str(i+2)].text == self.ids['b'+str(i+4)].text:
                    self.ids['b'+str(i)].color = "green"
                    self.ids['b'+str(i+2)].color = "green"
                    self.ids['b'+str(i+4)].color = "green"
                    self.end_game()

    def play(self, btn):
        self.button = btn
        if self.turn == "X":                # Switches between "X" and "O"
            btn.text = "X"                  # Sets button text to "X"
            btn.disabled = True             # Disables button in kvlang  on press
            self.ids.display.text = "O's Turn!"
            self.turn = "O"                 # Sets the next move to "O"
            self.no_winner()                # Checks if there's a winner after every move
            self.game_rules()
        else:
            btn.text = "O"
            btn.disabled = True
            self.ids.display.text = "X's Turn!"
            self.turn = "X"
            self.no_winner()
            self.game_rules()

    # A draw scenario
    def no_winner(self):
        disabled_btn = 0
        for i in range(1, 10):
            if self.ids['b'+str(i)].disabled and self.ids['b'+str(i)].text != "" and \
                    self.ids['b'+str(i)].color != "green":
                disabled_btn += 1
        if disabled_btn == 9:
            self.ids.display.text = "THAT\'S A TIE"

    def end_game(self):
        self.ids.restart.text = "NEXT ROUND"
        for i in range(1, 10):  # disables all buttons
            self.ids['b'+str(i)].disabled = True
        # if block to increment O's value by 2 per win round
        if self.turn == "X":
            self.turn = "O"
            self.ids.display.text = self.turn + " WINS!"
            self.ids.player2.value += 2
        # else block to increment X's value by 2 per win round
        elif self.turn == "O":
            self.turn = "X"
            self.ids.display.text = self.turn + " WINS!"
            self.ids.player1.value += 2
        # Condition block to display overall winner and reset round counter
        if self.ids.player1.value == 10:
            self.ids.display.text = "GAME OVER"
            self.ids.emptylabel.text = self.ids.Alias1.text + " WINS!"
            self.ids.restart.text = "RESTART"
            self.count = 0
        elif self.ids.player2.value == 10:
            self.ids.display.text = "GAME OVER"
            self.ids.emptylabel.text = self.ids.Alias2.text + " WINS!"
            self.ids.restart.text = "RESTART"
            self.count = 0

    def restart_game(self):
        self.count += 1
        self.turn = "X"
        self.ids.restart.text = "ROUND " + str(self.count)
        self.ids.display.text = "X GOES FIRST"
        # self.ids.display.text = ""
        if self.ids.player1.value == 10 or self.ids.player2.value == 10:
            self.ids.player1.value = 0
            self.ids.player2.value = 0
            self.ids.display.text = "X GOES FIRST"
            self.ids.emptylabel.text = ""
        # loop to enable all buttons, reset their color and text to "".
        for i in range(1, 10):
            self.ids['b' + str(i)].text = ""
            self.ids['b' + str(i)].color = 0, 0, 0, 0
            self.ids['b' + str(i)].disabled = False


class TicTacToeApp(App):
    # def build(self):
    #     sm = ScreenManager()
    #     sm.add_widget(MenuScreen(name="menuscreen"))
    #     sm.add_widget(T3Main(name="maingame"))
    #     sm.add_widget(MultiplayerScreen(name="multiplayerscreen"))
    #     return sm
    pass


TicTacToeApp().run()
