# Project: Python Terminal Battleship Game
# by: @Brohmarr

# A single-player terminal-based version of the famous "Battleship" game
#     where the user plays against an IA.

# TODOs:
# 
# [X] Create the "Game Master" class, that will control the game loop;
# [X] Generate the game board and randomize the positions of the ships;
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
        self.coordinates = []
        self.coordinates_state = []
    
    def __repr__(self):
        return "O" * self.size

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
        # Player-related data.
        self.player = Player(player_name)
        self.adversary = AdversaryAI()
        self.turn = "player"

        # Ship-related data.
        self.ships_sizes_by_quantity = {2: 4, 3: 3, 4: 2, 5: 1}
        self.ships = []
        for size in self.ships_sizes_by_quantity.keys():
            quantity = self.ships_sizes_by_quantity[size]
            if quantity != 0:
                for ship in range(quantity):
                    self.ships.append(Ship(size))

        # Board-related data.
        self.board_size = [10, 10]
        self.board = [["*" for i in range(self.board_size[1])]
                      for i in range(self.board_size[0])]
        self.hidden_board = [["*" for i in range(self.board_size[1])]
                             for i in range(self.board_size[0])]
        
        # Placing the ships in the board.
        for ship in self.ships:
            is_ship_placed = False
            while not is_ship_placed:
                # Getting the coordinates to place the current ship and
                #     checking if the coordinates above are occupied
                #     (considering the current ship's size).
                if ship.angle == 0:
                    x = rnd.randint(0, self.board_size[0] - 1 - ship.size)
                    y = rnd.randint(0, self.board_size[1] - 1)

                    ship_can_be_placed = True
                    for i in range(ship.size):
                        if self.hidden_board[x + i][y] != "*":
                            ship_can_be_placed = False
                            break
                    
                    # Now that we know the coordinates are available, place
                    #     the current ship there.
                    if ship_can_be_placed:
                        for i in range(ship.size):
                            ship.coordinates.append([x + i, y])
                            self.hidden_board[x + i][y] = "O"
                        
                        is_ship_placed = True
                else:
                    x = rnd.randint(0, self.board_size[0] - 1)
                    y = rnd.randint(0, self.board_size[1] - 1 - ship.size)

                    ship_can_be_placed = True
                    for i in range(ship.size):
                        if self.hidden_board[x][y + i] != "*":
                            ship_can_be_placed = False
                            break
                    
                    # Now that we know the coordinates are available, place
                    #     the current ship there.
                    if ship_can_be_placed:
                        for i in range(ship.size):
                            ship.coordinates.append([x, y + i])
                            ship.coordinates_state.append("OK")
                            self.hidden_board[x][y + i] = "O"
                        
                        is_ship_placed = True
    
    def display_board(self, board_to_show: list):
        print("       A  B  C  D  E  F  G  H  I  J" + "\n")
        for l_index, line in enumerate(board_to_show):
            for c_index, column in enumerate(line):
                if c_index == 0:
                    if l_index == (len(board_to_show) - 1):
                        print(str(l_index + 1) + "     ", end = "")
                    else:
                        print(" " + str(l_index + 1) + "     ", end = "")
                if c_index == (len(line) - 1):
                    print(column)
                else:
                    print(column + "  ", end = "")

    def display_game_window(self):
        print("Welcome to Battleship (the Single-Player Terminal-Based Version)!")
        print()
        print("Shoot: Type a letter from A to J followed by a space and a number from 1 to 10;")
        print("~ The one to give the final shot at a ship keeps all of its points (100 / tile).")
        print()
        self.display_board(self.board)
        print()
        # Make this part dynamic.
        print("Ships Remaining: 4x (O  O) ; 3x (O  O  O) ; 2x (O  O  O  O) ; 1x (O  O  O  O  O)")
        print("Score Board:")
        print("~ Player:    {player_score}".format(player_score = self.player.score))
        print("~ Adversary: {adversary_score}".format(adversary_score = self.adversary.score))
        print()
        print("~> Where do you want to shoot? ")

# TESTING PHASE

# Is the board setup correct? Yeap!
gm = GameMaster("Brohmarr")
print(gm.board)
print()
print(gm.ships)
print()
print(gm.hidden_board)
print()
for ship in gm.ships:
    print(ship.coordinates)
print()
gm.display_board(gm.board)
print()
gm.display_board(gm.hidden_board)
print()
gm.display_game_window()
