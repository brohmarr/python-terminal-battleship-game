# Project: Python Terminal Battleship Game
# by: @Brohmarr

# A single-player terminal-based version of the famous "Battleship" game
#     where the user plays against an IA.

# TODOs:
# 
# [X] Create the "Game Master" class, that will control the game loop;
# [X] Generate the game board and randomize the positions of the ships;
# [X] Display everything correctly in a regular terminal window (80x24);
# [X] Make the player able to shoot at a specific position in the board;
# [X] Create the points system;
# [ ] Create the "Adversary" (AI) game loop;
# [X] Make sure the game is finished when the last ship is destroyed.


import random as rnd

# This class holds the data for the ships.
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
    self.last_shot = []

# This class holds the data for the user.
class Player:

  # Initializing the player attributes.
  def __init__(self, name: str):
    self.name = name
    self.score = 0
    self.last_shot = []

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
  def __init__(self):
    # Creating the players (user + AI).
    player_name = input("Enter your name, please (limit of 14 characters): ")
    if len(player_name) > 14:
      player_name = player_name[:14]
    self.player = Player(player_name)
    self.adversary = AdversaryAI()
    self.turn = "player"
    self.game_over = False

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
  
  # Displays the last line of the game window, where the user will type in
  #     the coordinates.
  def display_player_input_line(self, message: str = "~> Where do you want to shoot? "):
    print(message, end = "")

  # Changes the ship's representation from 'o's to 'x's, add its size * 100
  #     to the score of the player that destroyed it and removes it from
  #     the list of remaining ships.
  def destroy_ship(self, ship: Ship):
    # Changing the ship's representation.
    for coord in ship.coordinates:
      x = coord[0]
      y = coord[1]
      self.board[x][y] = 'x'
    
    # Adding to the score board.
    if self.turn == "player":
      self.player.score += ship.size * 100
    else:
      self.adversary.score += ship.size * 100

    # Removing the ship from the game.
    self.ships.pop(self.ships.index(ship))

    # Checking if all the ships were destroyed to end the game.
    if len(self.ships) == 0:
      self.game_over_message()

  # Changes the game board to be the same as the randomly generated hidden
  #     one at the coordinates received.
  def update_board(self, x: int, y: int):
    # Setting the "displayed board" to be equal the randomly generated
    #     one, with the ships.
    self.board[x][y] = self.hidden_board[x][y]
    
    # Saving the coordinates of the current player's last successful shot.
    numbers_to_letters = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j'}
    
    if self.turn == "player":
      self.player.last_shot = [numbers_to_letters[y + 1].upper(), x + 1]
    else:
      self.adversary.last_shot = [x, y]

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

  def format_score(self, score: int) -> str:
    str_score = str(score)
    final_str = ""

    counter = 4 - len(str_score)
    while counter > 0:
      final_str += '0'
      counter -= 1
    
    return final_str + str_score

  # Prints the whole game information to the terminal.
  def display_game_window(self):
    # Adding a blank line just for precaution...
    print()

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
      if (len(ship.coordinates)) in ships_remaining_per_size:
        ships_remaining_per_size[(len(ship.coordinates))] += 1
      else:
        ships_remaining_per_size[(len(ship.coordinates))] = 1
    
    # Making sure their entries exists even if there are no more ships.
    if ships_remaining_per_size.get(2) == None:
      ships_remaining_per_size[2] = 0
    if ships_remaining_per_size.get(3) == None:
      ships_remaining_per_size[3] = 0
    if ships_remaining_per_size.get(4) == None:
      ships_remaining_per_size[4] = 0
    if ships_remaining_per_size.get(5) == None:
      ships_remaining_per_size[5] = 0

    print("{quantity_2}x (O  O) ; {quantity_3}x (O  O  O) ; {quantity_4}x (O  O  O  O) ; {quantity_5}x (O  O  O  O  O)".format(
      quantity_2 = ships_remaining_per_size[2],
      quantity_3 = ships_remaining_per_size[3],
      quantity_4 = ships_remaining_per_size[4],
      quantity_5 = ships_remaining_per_size[5]
    ))

    # Score board.
    print("Score Board: {player_name} ({player_score}) - {player_last_shot}, {adversary_name} ({adversary_score}) - {adversary_last_shot}".format(
      player_name = self.player.name,
      player_score = self.format_score(self.player.score),
      player_last_shot = self.player.last_shot,
      adversary_name = self.adversary.name,
      adversary_score = self.format_score(self.adversary.score),
      adversary_last_shot = self.adversary.last_shot
    ))
    print()

    # Legends.
    print("Legends: '*' = Untargeted ; '~' = Water ; 'o' = Ship ; 'x' = Destroyed Ship")
    print()

  # Checks if the received coordinates are valid or not.
  def check_if_coordinates_are_valid(self, possible_letters: dict, possible_numbers: range, x: str, y: int) -> bool:
    if x in possible_letters.keys() and y in possible_numbers:
      return True
    else:
      return False

  # Checks if the received coordinates are valid or not.
  def check_if_coordinates_are_targetable(self, x: int, y: int) -> bool:
    x -= 1
    y -= 1

    if self.board[x][y] == '~' or self.board[x][y] == 'x' or self.board[x][y] == 'o':
      return False
    
    else:
      return True

  # Converts the string input received from the user to 'x' and 'y' coordinates.
  def convert_input_to_coordinates(self, coord_to_shoot: str) -> tuple:
    while True:
      letters_to_numbers = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10}

      # Separating the x axis from the y axis.
      coords = coord_to_shoot.split()

      # Making sute the input is valid.
      while len(coords) < 2:
        self.display_game_window()
        self.display_player_input_line("These coordinates are not valid. Please, choose another one: ")
        coord_to_shoot = input()
        
        # Checking if the input was given following the correct instructions:
        #     [LETTER][SPACE][NUMBER]
        coords = coord_to_shoot.split()
        if len(coords) >= 2 and not coords[1].isdigit():
          coord_to_shoot = ""
          coords = []

      # Checking if the coordinates received are valid.
      if self.check_if_coordinates_are_valid(letters_to_numbers, range(1, 11), coords[0].lower(), int(coords[1])):
        # Transforming the letter from the x axis to an integer.
        y = letters_to_numbers[coords[0].lower()]
        
        # Transforming the "string number" from the y axis to an integer.
        x = int(coords[1])

        # Checking if the coordinates have already been hit.
        if self.check_if_coordinates_are_targetable(x, y):
          return x, y
        
        else:
          self.display_game_window()
          self.display_player_input_line("These coordinates were already targeted. Please, choose another one: ")
          coord_to_shoot = input()

      # If the coordinates are not valid, ask for input again.
      else:
        self.display_game_window()
        self.display_player_input_line("These coordinates are not valid. Please, choose another one: ")
        coord_to_shoot = input()

  # Displays what was hidden in the chosen coordinates. 
  def shoot_at_coordinates(self, x: int, y: int):
    is_shot_fired = False
    while not is_shot_fired:
      # Checking if the received coordinates have not been targeted before.
      if self.check_if_coordinates_are_targetable(x, y):
        self.update_board(x - 1, y - 1)
        is_shot_fired = True
      else:
        self.display_game_window()
        self.display_player_input_line("These coordinates were already targeted. Please, choose another one: ")
        new_coords = input()
        x, y = self.convert_input_to_coordinates(new_coords)

        continue
  
  # Ends the game.
  def game_over_message(self):
    # Checking who was the winner (the one with the highest score).
    winner = Player("None")
    if self.player.score > self.adversary.score:
      winner = self.player
    else:
      winner = self.adversary
    
    # Creating the final message to the player based on the winner of the match.
    final_message = "Game Over! {winner_name} is the winner with {winner_score} points! Press 'e' to exit: ".format(
      winner_name = winner.name,
      winner_score = winner.score
    )
    
    # Asking the player to exit the game.
    input_to_end_it = ''
    while input_to_end_it.lower() != 'e':
      self.display_game_window()
      self.display_player_input_line(final_message)
      input_to_end_it = input()
    
    # Game Over!
    self.game_over = True


# TESTING PHASE
# def testing():
#   # Is the board setup correct? Yeap!
#   gm = GameMaster()

#   # Is the board being printed correctly with and without the ships? Yeap!
#   print(gm.board)
#   print()
#   print(gm.ships)
#   print()
#   print(gm.hidden_board)
#   print()

#   # Are the ships being positioned correctly in the board (no overlap)? Yeap!
#   for ship in gm.ships:
#     print(ship.coordinates)
#   print()
#   gm.display_board(gm.board)
#   print()
#   gm.display_board(gm.hidden_board)
#   print()

#   # Is the game window being displayed correctly? Yeap!
#   # gm.display_game_window()
#   # gm.ships.pop(0)
#   # gm.display_game_window()
#   # gm.display_player_input_line()
#   # print()

#   # Is the shoot function working? Yeap!
#   gm.shoot_at_coordinates(5, 5)
#   gm.display_game_window()
#   gm.display_player_input_line()

#   # Is the player able to shoot? Yeap!
#   gm.shoot_at_coordinates(5, 5)

#   # Is the ship destroyable?
#   while len(gm.ships) == 10:
#     gm.display_game_window()
#     gm.display_player_input_line()
#     target = input()
#     x, y = gm.convert_input_to_coordinates(target)
#     gm.shoot_at_coordinates(x, y)
#   gm.display_game_window()
#   print(gm.ships)

# TESTING THE GAME OVER FUNCTION
# def testing_game_over():
#   gm = GameMaster()
  
#   gm.ships = [gm.ships[0]]
  
#   print(gm.ships[0].coordinates)

#   while not gm.game_over:
#     # Display the game window.
#     gm.display_game_window()
#     gm.display_player_input_line()
    
#     # Get the player input.
#     target = input()
    
#     # Convert it to coordinates in the game board.
#     x, y = gm.convert_input_to_coordinates(target)
    
#     # Shoot at those coordinates.
#     gm.shoot_at_coordinates(x, y)


# MAIN
def main():
  gm = GameMaster()

  while not gm.game_over:
    if gm.turn == "player":
      # Display the game window.
      gm.display_game_window()
      gm.display_player_input_line()

      # Get the player input.
      target = input()

      # Convert it to coordinates in the game board.
      x, y = gm.convert_input_to_coordinates(target)

      # Shoot at those coordinates.
      gm.shoot_at_coordinates(x, y)
    
    else:
      # The adversary (AI) make their shot.
      pass #TODO: Complete this!


# Testing the code...
#testing()
#testing_game_over()

# Starting the game...
main()
