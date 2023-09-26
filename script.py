# Project: Python Terminal Battleship Game
# by: @Brohmarr

# A single-player terminal-based version of the famous "Battleship" game
#     where the user plays against an IA.

# TODOs:
# 
# [X] Create the "Game Master" class, that will control the game loop;
# [ ] Generate the game board and randomize the positions of the ships;
# [ ] Display everything correctly in a regular terminal window (80x24);
# [ ] Make the player able to shoot at a specific position in the board;
# [ ] Create the points system;
# [ ] Create the "Adversary" (AI) game loop;
# [ ] Make sure the game is finished when the last ship is destroyed.


import random as rnd

# This class holds the data for the ships that will be hidden.
class Ship:
    def __init__(self, size: int):
        self.size = size
        self.angle = rnd.randint(0, 1)

# This class holds the data for the player's opponent.
class AdversaryAI:
    def __init__(self):
        self.name = "General Robson"
        self.score = 0

# This class holds the data for the user.
class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

# This class controls the game loop.
class GameMaster:
    def __init__(self, player_name: str):
        self.player = Player(player_name)
        self.adversary = AdversaryAI()
        self.turn = "player"
        self.board_size = [10, 10]
        self.board = [["*" for i in range(self.board_size[1])]
                      for i in range(self.board_size[0])]

# TESTING PHASE

# Is the board setup correct? Yeap!
gm = GameMaster("Brohmarr")
print(gm.board)
