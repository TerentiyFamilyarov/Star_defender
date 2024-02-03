import Player
import main_game


class Disasters:
    def __init__(self):
        self.MainGame = main_game.GameWindow()
    def SlowDown(self, step):
            self.MainGame.player1.step -= step
    def U_Windy(self):
        s=0
    def D_Windy(self):
        s=0