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

    # Remembers if an specific coordinate of the ship is "hit" or "ok".
    self.coordinates_state = []
    
  # Settings the print option to the size of the ship using the character "O".
  def __repr__(self):
    return 'o' * self.size

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
        if self.hidden_board[x + (i * x_axis)][y + (i * y_axis)] != '~':
          ship_can_be_placed = False
          break

      # Placing the ship in the randomized coordinates if they are available.
      if ship_can_be_placed:
        for i in range(ship.size):
          ship.coordinates.append([x + (i * x_axis), y + (i * y_axis)])
          ship.coordinates_state.append("ok")
          self.hidden_board[x + (i * x_axis)][y + (i * y_axis)] = 'o'

          is_ship_placed = True

  # Initializing the game master (GM) attributes.
  def __init__(self, player_name: str):
    # Creating the players (user + AI).
    self.player = Player(player_name)
    self.adversary = AdversaryAI()
    self.turn = "player"

    # Creating the ships.
    self.ships_sizes_by_quantity = {2: 4, 3: 3, 4: 2, 5: 1}
    self.ships = []
    for size in self.ships_sizes_by_quantity.keys():
      quantity = self.ships_sizes_by_quantity[size]
      if quantity != 0:
        for ship in range(quantity):
          self.ships.append(Ship(size))

    # Creating the board.
    self.board_size = [10, 10]
    self.board = [['*' for i in range(self.board_size[1])] for i in range(self.board_size[0])]
    self.hidden_board = [['~' for i in range(self.board_size[1])] for i in range(self.board_size[0])]
    
    # Placing the ships in the board.
    for ship in self.ships:
      if ship.angle == 0:
        self.place_ship(ship, 1, 0)
      else:
        self.place_ship(ship, 0, 1)
  
  def display_player_input_line(self, message: str = "~> Where do you want to shoot? "):
    print(message, end = "")

  # TODO: Comment this!
  def destroy_ship(self, ship: Ship):
    for coordinates in ship:
      x = coordinates[0]
      y = coordinates[1]
      self.board[x][y] = 'x'
    self.ships.pop(ship)

  # TODO: Comment this!
  def update_board(self, x: int, y: int):
    # Setting the "displayed board" to be equal the randomly generated one, with the ships.
    self.board[x][y] = self.hidden_board[x][y]

    # Checking if a ship was hit, to update its status.
    if self.board[x][y] == 'o':
      for ship in self.ships:
        for coordinate in ship.coordinates:
          if coordinate == [x, y]:
            ship.coordinates_state[ship.coordinates.index([x, y])] = "hit"

            is_ship_destroyed = True
            for state in ship.coordinates_state:
              if state == "ok":
                is_ship_destroyed = False
            
            if is_ship_destroyed:
              self.destroy_ship(ship)

  # Prints the board to the terminal.
  def display_board(self, board_to_show: list):
    # Adding a blank line just for precaution...
    print()
    
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
    print("    {player_name}: {player_score}".format(
      player_name = self.player.name,
      player_score = self.player.score
    ))
    print("    {adversary_name}: {adversary_score}".format(
      adversary_name = self.adversary.name,
      adversary_score = self.adversary.score
    ))
    print()

  # TODO: Comment this later!
  def convert_input_to_coordinates(self, coord_to_shoot: str) -> tuple:
    letters_to_numbers = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10}
    
    # Separating the x axis from the y axis.
    coords = coord_to_shoot.split()

    # Transforming the letter from the x axis to an integer.
    x = letters_to_numbers[coords[0].lower()]
    
    # Transforming the "string number" from the y axis to an integer.
    y = int(coords[1])

    if self.check_if_coordinates_are_valid(x, y):
      return x, y

  # TODO: Comment this later!
  def check_if_coordinates_are_valid(self, x: int, y: int) -> bool:
    x -= 1
    y -=1

    if self.board[x][y] == '~' or self.board[x][y] == 'x' or self.board[x][y] == 'o':
      self.display_board(self.board)
      self.display_player_input_line("These coordinates were already targeted. Please, choose another one: ")
      
      return False
    
    else:
      return True

  # TODO: Comment this!
  def shoot_at_coordinates(self, x: int, y: int):
    is_shot_fired = False
    while not is_shot_fired:
      # Checking if the received coordinates have not been targeted before.
      if self.check_if_coordinates_are_valid(x, y):
        self.update_board(x - 1, y - 1)
        is_shot_fired = True
      else:
        new_coords = input()
        x, y = self.convert_input_to_coordinates(new_coords)

        continue


# TESTING PHASE
def testing():
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
  gm.display_player_input_line()
  print()

  # Is the shoot function working?
  gm.shoot_at_coordinates(5, 5)
  gm.display_game_window()
  gm.display_player_input_line()

  # Is the player able to shoot?

# MAIN
def main():
  # TODO: Start the game here...
  pass


# Testing the code...
testing()

# Starting the game...
#main()
