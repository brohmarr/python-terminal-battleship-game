# Project: Python Terminal Battleship Game
# by: @Brohmarr

# A single-player terminal-based version of the famous "Battleship" game
#     where the user plays against an IA.

# TODOs:
# 
# [X] Create the "Game Master" class, that will control the game loop;
# [X] Generate the game board and randomize the positions of the ships;
# [X] Display everything correctly in a regular terminal window (80x24);
# [ ] Make the player able to shoot at a specific position in the board;
# [ ] Create the points system;
# [ ] Create the "Adversary" (AI) game loop;
# [ ] Make sure the game is finished when the last ship is destroyed.


import random as rnd

# This class holds the data for the ships that will be hidden.
class Ship:

  # Initializing the ship attributes.
  def __init__(self, size: int):
    self.size = size

    # Decides if the ship should be placed horizontally (0) or vertically (1).
    self.angle = rnd.randint(0, 1)

    # The coordinates of the ship.
    self.coordinates = []

    # Remembers if an specific coordinate of the ship was "hit" or is "ok".
    self.coordinates_state = []
    
  # Settings the print option to the size of the ship using the character "O".
  def __repr__(self):
    return "O" * self.size

# This class holds the data for the player's opponent.
class AdversaryAI:

  # Initializing the adversary attributes.
  def __init__(self):
    self.name = "General Robson"
    self.score = 0

# This class holds the data for the user.
class Player:

  # Initializing the player attributes.
  def __init__(self, name: str):
    self.name = name
    self.score = 0

# This class controls the game loop.
class GameMaster:

  # Places a ship in the game board based on their angle.
  def place_ship(self, ship: Ship, x_axis: int, y_axis: int):
    is_ship_placed = False
    while not is_ship_placed:
      # Getting the coordinates to place the current ship into the board.
      x = rnd.randint(0, self.board_size[0] - 1 - (ship.size * x_axis))
      y = rnd.randint(0, self.board_size[1] - 1 - (ship.size * y_axis))

      # Checking if the coordinates above are occupied using the size of the ship.
      ship_can_be_placed = True
      for i in range(ship.size):
        if self.hidden_board[x + (i * x_axis)][y + (i * y_axis)] != "*":
          ship_can_be_placed = False
          break

      # Placing the ship in the randomized coordinates if they are available.
      if ship_can_be_placed:
        for i in range(ship.size):
          ship.coordinates.append([x + (i * x_axis), y + (i * y_axis)])
          ship.coordinates_state.append("OK")
          self.hidden_board[x + (i * x_axis)][y + (i * y_axis)] = "O"

          is_ship_placed = True

  # Initializing the game master (GM) attributes.
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
    self.board = [["*" for i in range(self.board_size[1])] for i in range(self.board_size[0])]
    self.hidden_board = [["*" for i in range(self.board_size[1])] for i in range(self.board_size[0])]
    
    # Placing the ships in the board.
    for ship in self.ships:
      if ship.angle == 0:
        self.place_ship(ship, 1, 0)
      else:
        self.place_ship(ship, 0, 1)
  
  # Prints the board to the terminal.
  def display_board(self, board_to_show: list):
    # Display the letters of the board (columns).
    print("       A  B  C  D  E  F  G  H  I  J" + "\n")

    # For every line in the board, do...
    for l_index, line in enumerate(board_to_show):
      # For every column in the board, do...
      for c_index, column in enumerate(line):
        # If its the first column...
        if c_index == 0:
          # ... print this way...
          if l_index == (len(board_to_show) - 1):
            print(str(l_index + 1) + "     ", end = "")
          
          # ... or this way if it's the line number "10".
          else:
            print(" " + str(l_index + 1) + "     ", end = "")
                
        # If its the last column, just print its data.
        if c_index == (len(line) - 1):
          print(column)
                
        # If its not the last column, print its data + the empty space.
        else:
          print(column + "  ", end = "")

  # Prints the whole game information to the terminal.
  def display_game_window(self):
    # Greeting.
    print("Welcome to Battleship (the Single-Player Terminal-Based Version)!")
    print()
        
    # Rules.
    print("Shoot: Type a letter from A to J followed by a space and a number from 1 to 10;")
    print("~ The one to give the final shot at a ship keeps all of its points (100 / tile).")
    print()
        
    # Board.
    self.display_board(self.board)
    print()

    # Remaining ships.
    print("Ships Remaining: ", end = "")
    ships_remaining_per_size = {}
    for ship in self.ships:
      if (len(ship.coordinates) - 2) in ships_remaining_per_size:
        ships_remaining_per_size[(len(ship.coordinates) - 2)] += 1
      else:
        ships_remaining_per_size[(len(ship.coordinates) - 2)] = 1
    print("{quantity_2}x (O  O) ; {quantity_3}x (O  O  O) ; {quantity_4}x (O  O  O  O) ; {quantity_5}x (O  O  O  O  O)".format(
      quantity_2 = ships_remaining_per_size[0],
      quantity_3 = ships_remaining_per_size[1],
      quantity_4 = ships_remaining_per_size[2],
      quantity_5 = ships_remaining_per_size[3]
    ))

    # Score board.
    print("Score Board:")
    print("~ {player_name}: {player_score}".format(
      player_name = self.player.name,
      player_score = self.player.score
    ))
    print("~ {adversary_name}: {adversary_score}".format(
      adversary_name = self.adversary.name,
      adversary_score = self.adversary.score
    ))
    print()

    # Player input line.
    print("~> Where do you want to shoot? ")

# TESTING PHASE

# Is the board setup correct? Yeap!
gm = GameMaster("Brohmarr")

# Is the board being printed correctly with and without the ships? Yeap!
print(gm.board)
print()
print(gm.ships)
print()
print(gm.hidden_board)
print()

# Are the ships being positioned correctly in the board (no overlap)? Yeap!
for ship in gm.ships:
  print(ship.coordinates)
print()
gm.display_board(gm.board)
print()
gm.display_board(gm.hidden_board)
print()

# Is the game window being displayed correctly? Yeap!
gm.display_game_window()
gm.ships.pop(0)
gm.display_game_window()
